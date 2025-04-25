import inspect
from typing import Any, Callable, Mapping, Optional, override
from scipy.optimize import minimize
import pandas as pd

from .profiling.profiler import PvradarProfiler
from .utils import convert_by_attrs
from .model_wrapper import ModelBinding, ModelWrapper
from .optimization import OptimizationSeriesTarget, OptimizationTarget
from .basics import BindingNotFound, EmptyBinding, LambdaArgument, ModelConfig, ModelParam
from .resource_type_helpers import ResourceTypeDescriptor, ResourceTypeClass
from .base_model_context import BaseModelContext, Hook
from .sweeps.sweep_types import SweepRange
from .sweeps.sync_sweep_iterator import SyncSweepIterator
from ..common.exceptions import PvradarSdkException
from .hooks import attrs_as_descriptor_mapping, hook_binder, HookSelection, preprocess_bind_resource_input

MAX_DEPTH = 50


def known_model_binder(
    *,
    resource_name: str,
    as_param: Optional[ModelParam] = None,
    defaults: Optional[dict[str, Any]] = None,
    context: Optional[Any] = None,
) -> Any:
    if context is None:
        return BindingNotFound
    name = resource_name
    if name in context.models and not context.models[name].config.get('disable_auto_resolve', False):
        return ModelBinding(model=context.models[name], defaults=defaults or {})
    return BindingNotFound


class ModelContext(BaseModelContext):
    def __init__(self, id: Optional[str] = None, **kwargs) -> None:
        super().__init__()
        self.models: dict[str, ModelWrapper] = {}
        self._resources: dict[str, Any] = dict(kwargs)
        self.binders: list[Callable] = [hook_binder, known_model_binder]
        self.config: ModelConfig = {}
        self.mapping_by_resource_types: dict[str, ModelWrapper] = {}
        self.id = id
        self._locks = {}

    def hooks(self, *args: Hook) -> HookSelection:
        return HookSelection(self, list(args))

    @override
    def register_model(
        self,
        model: Callable,
        *,
        defaults: Optional[dict[str, Any]] = None,
        for_resource_type: Optional[str | bool] = None,
    ) -> ModelWrapper:
        if not isinstance(model, ModelWrapper):
            model = ModelWrapper(model, defaults)
        if defaults is None:
            defaults = {}
        self.models[model.name] = model
        if for_resource_type:
            if for_resource_type is True:
                for_resource_type = getattr(model, 'resource_type', None)
                if not for_resource_type:
                    raise ValueError(
                        'Model {mode.name} not have resource_type set. '
                        + 'Use @resource_type decorator or explicit for_resource_type="..."'
                    )
            assert isinstance(for_resource_type, str)
            self.mapping_by_resource_types[for_resource_type] = model
        return model

    @override
    def wrap_model(self, model: Callable | str) -> ModelWrapper:
        if isinstance(model, str):
            if model not in self.models:
                raise LookupError(f'Model {model} not found')
            model = self.models[model]
        if not isinstance(model, ModelWrapper):
            model = ModelWrapper(model)
        return model

    def bind_params_with_defaults(
        self,
        model: ModelWrapper,
        __config__: Optional[ModelConfig] = None,
        **kwargs,
    ) -> dict[str, Any]:
        defaults = model.defaults.copy()
        defaults.update(kwargs)
        return self.bind_params(params=model.params, defaults=defaults, for_model=model.name, __config__=__config__)

    def _convert_by_attrs(self, value: Any, param_attrs: Mapping[str, Any]) -> Any:
        """wrapper around convert_by_attrs to allow for context level overrides (e..g validation for PvradarSite)"""
        return convert_by_attrs(value, param_attrs)

    def _process_output(self, model: ModelWrapper, bound_params: dict[str, Any], result: Any) -> Any:
        if model.return_param.attrs:
            result = self._convert_by_attrs(result, model.return_param.attrs)
            if isinstance(result, pd.Series) or isinstance(result, pd.DataFrame):
                if 'resource_type' in model.return_param.attrs:
                    result.attrs['resource_type'] = model.return_param.attrs['resource_type']
        for output_filter in self.output_filters:
            result = output_filter(model, bound_params, result)
        return result

    def _process_input(self, model: ModelWrapper, param: ModelParam, value: Any) -> Any:
        if param.attrs is not None:
            value = self._convert_by_attrs(value, param.attrs)
            if param.attrs.get('keep', False):
                if param.name == '_anonymous':
                    raise ValueError('Cannot keep anonymous parameter')
                self._resources[param.name] = value
        return value

    @override
    def run(self, model: Callable | str, _depth: int = 0, **kwargs):
        if (_depth := _depth + 1) > MAX_DEPTH:
            raise RecursionError(f'ModelContext.run max recursions reached: {MAX_DEPTH}')

        model = self.wrap_model(model)
        bound_params = self.bind_params_with_defaults(model, **kwargs)

        # execute all model bindings
        for k, v in bound_params.items():
            if isinstance(v, ModelBinding):
                combined_defaults = v.defaults.copy()
                combined_defaults.update(bound_params)
                bound_params[k] = self.run(v.model, _depth=_depth, **combined_defaults)  # type: ignore

        for k, v in bound_params.items():
            bound_params[k] = self._process_input(model, model.params[k], v)

        if not self.config.get('disable_validation'):
            model.validate(**bound_params)
        result = model(**bound_params)
        result = self._process_output(model, bound_params, result)
        return result

    def merge_config(self, config: Optional[ModelConfig]):
        if not config:
            return self.config
        result = self.config.copy()
        result.update(config)
        return result

    @override
    def resource(
        self,
        name: Any,
        *,
        attrs: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ) -> Any:
        if attrs is None:
            attrs = {}
        if isinstance(name, (dict, ResourceTypeClass, ResourceTypeDescriptor)):
            if attrs:
                raise ValueError(
                    'two attrs arguments provided, either use .resource(name, attrs={...atr}) or .resource({...attr})'
                )
            attrs = attrs_as_descriptor_mapping(name)
            name = '_anonymous'

        # if resource was requested as dict, then it was converted to _anonymous
        # so from here on name is only str
        assert isinstance(name, str), 'resource name must be a string'

        if name in self._resources:
            result = self._resources[name]
            if attrs:
                result = self._convert_by_attrs(result, attrs)
            return result
        v, new_as_param = self._bind_resource(name, as_param=ModelParam(name=name, annotation=None, attrs=attrs))

        if BindingNotFound.check(v):
            reported_attrs = attrs
            if new_as_param and new_as_param.attrs:
                reported_attrs = new_as_param.attrs
            if name == '_anonymous':
                raise LookupError(f'Unknown method to calculate resource for: {reported_attrs}')
            raise LookupError(f'Unknown method to calculate "{name}" with: {reported_attrs}')
        if isinstance(v, ModelBinding):
            combined_defaults = v.defaults.copy()
            if 'params' in attrs:
                combined_defaults.update(attrs['params'])
            combined_defaults.update(kwargs)
            result = self.run(v.model, **combined_defaults)
            if attrs:
                result = self._convert_by_attrs(result, attrs)
            return result
        else:
            return v

    def _bind_resource(
        self,
        name: str,
        as_param: Optional[ModelParam] = None,
        __config__: Optional[ModelConfig] = None,
        defaults: Optional[dict[str, Any]] = None,
    ) -> tuple[Any, Optional[ModelParam]]:
        if defaults is None:
            defaults = {}
        me = self
        if __config__:
            me = self.copy()
            me.config = self.merge_config(__config__)

        if as_param and as_param.attrs and 'params' in as_param.attrs:
            defaults = defaults.copy()
            defaults.update(as_param.attrs['params'])

        if name == 'context':
            return me, as_param
        elif name in me._resources:
            return me._resources[name], as_param

        if as_param and as_param.attrs:
            as_param, defaults = preprocess_bind_resource_input(context=self, as_param=as_param, defaults=defaults)

        if as_param and isinstance(as_param.lambda_argument, LambdaArgument):
            return ModelBinding(
                model=self.wrap_model(self._lambda_argument_reader(as_param)),
                defaults=defaults or {},
            ), as_param

        for b in self.binders:
            result = b(resource_name=name, as_param=as_param, defaults=defaults, context=me)
            if BindingNotFound.check(result) or (result is None):
                continue
            if result is EmptyBinding:
                return None, as_param
            return result, as_param
        if self.mapping_by_resource_types and as_param and as_param.attrs and 'resource_type' in as_param.attrs:
            if as_param.attrs['resource_type'] in self.mapping_by_resource_types:
                return (
                    ModelBinding(
                        model=self.mapping_by_resource_types[as_param.attrs['resource_type']], defaults=defaults or {}
                    ),
                    as_param,
                )
        if as_param and as_param.default != inspect.Parameter.empty:
            return as_param.default, as_param
        return BindingNotFound, as_param

    def bind_params(
        self,
        *,
        params: dict[str, ModelParam],
        defaults: dict[str, Any],
        for_model: Optional[str] = None,
        __config__: Optional[ModelConfig] = None,
    ) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for k in params.keys():
            if k == 'return':
                continue
            elif k == 'kwargs':
                raise ValueError('Models may not have **kwargs as a parameter. Please use explicit names')
            elif k in defaults:
                result[k] = defaults[k]
            else:
                result[k], new_as_param = self._bind_resource(
                    name=k,
                    as_param=params[k],
                    defaults=defaults,
                    __config__=__config__,
                )

            if BindingNotFound.check(result[k]):
                config = self.merge_config(__config__)
                if 'ignore_missing_params' in config:
                    result.pop(k)
                    continue
                raise ValueError(f'Cannot bind parameter {k} for model {for_model}, known defaults: {list(defaults.keys())}')
        return result

    # override this method to handle special resource types like location and interval
    def on_resource_set(self, key: str, value: Any) -> Any:
        if key in self._locks:
            raise PvradarSdkException(f'Cannot set "{key}", it is locked')
        return value

    def lock(self, key: str) -> None:
        if key in self._locks:
            self._locks[key] += 1
        else:
            self._locks[key] = 1

    def unlock(self, key: str) -> None:
        if key in self._locks:
            level = self._locks[key] - 1
            if level <= 0:
                del self._locks[key]
            else:
                self._locks[key] = level

    def check_locked(self, key: str) -> bool:
        return key in self._locks

    @override
    def __setitem__(self, key, value):
        if key == 'context':
            raise ValueError('Cannot set context, it always refers to self')
        elif key == 'return':
            raise ValueError('Cannot set "return". It is a reserved keyword')
        elif key == 'kwargs':
            raise ValueError('Cannot set "kwargs". It is a reserved keyword')
        value = self.on_resource_set(key, value)
        self._resources[key] = value

    @override
    def __getitem__(self, key):
        return self._resources[key]

    @override
    def __delitem__(self, key):
        del self._resources[key]

    @override
    def __contains__(self, key):
        return key in self._resources

    @override
    def __iter__(self):
        return iter(self._resources)

    @override
    def __len__(self):
        return len(self._resources)

    def copy(self) -> 'ModelContext':
        c = ModelContext()
        c.models = self.models.copy()
        c.binders = self.binders.copy()
        c._resources = self._resources.copy()
        return c

    def update(self, other: Mapping) -> None:
        self._resources.update(other)

    def find_missing_param_names(
        self,
        model: Callable | str,
        __config__: Optional[ModelConfig] = None,
        **kwargs,
    ) -> list[str]:
        model = self.wrap_model(model)
        c: ModelConfig = {'ignore_missing_params': True}
        bound_params = self.bind_params_with_defaults(model, __config__=c, **kwargs)
        missing = []
        for k in model.params.keys():
            if k not in bound_params:
                missing.append(k)
        return missing

    def make_objective_function(
        self,
        model: Callable | str,
        *,
        target: OptimizationTarget,
        param_names: list[str],
        _verbosity: int = 0,
        **kwargs,
    ) -> Callable:
        model = self.wrap_model(model)
        context = self.copy()

        def objective_function(params):
            result = context.run(model, **kwargs, **dict(zip(param_names, params)))
            deviation = target.deviation(result)
            if _verbosity > 0:
                print(f'params: {params}, deviation: {deviation}')
            return deviation

        return objective_function

    def _lambda_argument_reader(
        self,
        model_param: ModelParam,
    ):
        def reader():
            """Callback for ModelBinding of a LambdaArgument"""
            la = model_param.lambda_argument
            assert la is not None
            new_model_param = ModelParam(
                name='_anonymous',
                type=la.type,
            )
            subject = self._get_resource_by_param(new_model_param)
            result = la.callable(subject)
            if model_param.attrs:
                result = self._convert_by_attrs(result, model_param.attrs)
            return result

        return reader

    def _get_resource_by_param(self, param: ModelParam) -> Any:
        """For now only used for LambdaArgument"""
        v, new_as_param = self._bind_resource('_anonymous', as_param=param)

        if BindingNotFound.check(v):
            raise LookupError(f'Unknown method to calculate parameter {param}')
        if isinstance(v, ModelBinding):
            result = self.run(v.model, **v.defaults)
            return result
        else:
            return v

    def sweep(self, target: Callable | str | dict, dimensions: SweepRange | list[SweepRange], **kwargs) -> SyncSweepIterator:
        resolved_targets = []
        if isinstance(target, dict):
            resolved_targets.append(target)
        elif callable(target) or isinstance(target, str):
            resolved_targets.append(self.wrap_model(target))
        else:
            raise ValueError(f'Invalid sweep target {target}')

        if isinstance(dimensions, dict):
            dimensions = [dimensions]

        return SyncSweepIterator(
            context=self,
            _targets=resolved_targets,
            _ranges=dimensions,
            **kwargs,
        )

    def optimize(
        self,
        model: Callable | str,
        *,
        target: OptimizationTarget | pd.Series,
        param_names: list[str] = [],
        _verbosity: int = 0,
        **kwargs,
    ) -> dict[str, Any]:
        if isinstance(target, pd.Series):
            target = OptimizationSeriesTarget(target)
        model = self.wrap_model(model)
        if not param_names:
            param_names = self.find_missing_param_names(model, **kwargs)
            if not param_names:
                raise ValueError('Failed detecting missing parameters, please provide param_names')

        objective_function = self.make_objective_function(
            model,
            target=target,
            param_names=param_names,
            _verbosity=_verbosity,
            **kwargs,
        )
        bounds = model.make_optimization_bounds(param_names)
        start_vector = model.make_start_vector(param_names, bounds)
        minimize_output = minimize(objective_function, start_vector, method='nelder-mead', bounds=bounds)
        auto_result = dict(zip(param_names, minimize_output.x))
        return auto_result

    def profile(self, subject: Any, **kwargs) -> PvradarProfiler:
        with PvradarProfiler(self) as profiler:
            if isinstance(subject, (dict, ResourceTypeClass, ResourceTypeDescriptor)):
                self.resource(subject, **kwargs)
            elif callable(subject) or isinstance(subject, str):
                self.run(subject, **kwargs)
            else:
                raise ValueError(f'Unsupported profiling subject type {type(subject)}')
            return profiler
