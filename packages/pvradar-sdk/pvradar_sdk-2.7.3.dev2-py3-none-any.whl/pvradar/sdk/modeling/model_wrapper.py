import inspect
import math
from dataclasses import dataclass, field
from typing import Annotated, Any, Optional, Self, Tuple, override

import numpy as np
from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo
from annotated_types import Gt, Ge, Lt, Le


from .introspection import attrs_from_annotation, lambda_argument_from_annotation, type_from_annotation
from .basics import Datasource, ModelConfig, ModelParam


class ModelWrapper:
    """
    Wraps a function (model) with additional metadata and validation.
    The wrapper can be used as drop-in replacement for the original function, as it implements the __call__ method.
    The ModelContext automatically wraps all functions with this class upon registration
    """

    def __init__(
        self,
        func: Any,
        defaults: Optional[dict[str, Any]] = None,
        __config__: Optional[ModelConfig] = None,
    ):
        self.config: ModelConfig = __config__ or {}
        self._func = func
        self.defaults: dict[str, Any] = defaults or {}
        (self.params, self.return_param) = self._introspect_func()
        self.validation_model = None

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    @override
    def __repr__(self):
        return f'<model:{self.name:}({self._param_summary()})>'

    @property
    def __annotations__(self):  # type: ignore
        return self._func.__annotations__

    def _param_summary(self):
        return ','.join([f'{p.name}' for p in self.params.values()])

    def _make_pydantic_model(self) -> None:
        f = self._func
        fields: dict = {}
        for k in f.__annotations__:
            v = f.__annotations__[k]
            if isinstance(v, type(Annotated[Any, Any])):  # type: ignore
                if hasattr(v, '__metadata__'):
                    for maybe_field in v.__metadata__:  # type: ignore
                        if isinstance(maybe_field, FieldInfo):
                            fields[k] = (v, maybe_field)
        if fields:
            self.validation_model = create_model(
                self.name,
                __config__={'arbitrary_types_allowed': True},
                **fields,
            )
        else:
            self.validation_model = None

    @property
    def resource_type(self) -> str | None:
        return self._func.resource_type if hasattr(self._func, 'resource_type') else None

    @property
    def name(self) -> str:
        return self._func.name if hasattr(self._func, 'name') else self._func.__name__

    @property
    def datasource(self) -> Datasource | None:
        return self._func.datasource if hasattr(self._func, 'datasource') else None

    @property
    def label(self) -> str:
        return self._func.label if hasattr(self._func, 'label') else self.name

    def _introspect_func(self) -> Tuple[dict[str, ModelParam], ModelParam]:
        params: dict[str, ModelParam] = {}
        signature = inspect.signature(self._func)
        for k in signature.parameters:
            default = signature.parameters[k].default
            if k in self.defaults:
                default = self.defaults.get(k)
            annotation = signature.parameters[k].annotation
            params[k] = ModelParam(
                name=k,
                annotation=annotation,
                default=default,
                attrs=attrs_from_annotation(annotation) or {},
                type=type_from_annotation(annotation),
                lambda_argument=lambda_argument_from_annotation(annotation),
            )
        return_param = ModelParam(
            name='return',
            annotation=signature.return_annotation,
            attrs=attrs_from_annotation(signature.return_annotation) or {},
            type=type_from_annotation(signature.return_annotation),
        )
        return (params, return_param)

    @property
    def pydantic_model(self) -> type[BaseModel] | None:
        if not self.validation_model:
            self._make_pydantic_model()
        return self.validation_model

    def validate(self, **kwargs):
        pm = self.pydantic_model
        if pm:
            pm(**kwargs)

    def _get_start_value(self, param_name: str, bound: Optional[tuple[float, float]] = None) -> float:
        if param_name in self.defaults:
            return self.defaults[param_name]
        if param_name in self.params:
            val = self.params[param_name].default
            if val is not None and val != inspect.Parameter.empty:
                return val
        if bound:
            if bound[0] != -np.inf and bound[1] != np.inf:
                return (bound[0] + bound[1]) / 2
            if bound[0] != -np.inf:
                return bound[0]
            if bound[1] != np.inf:
                return bound[1]
        return 0.0

    def _make_optimization_bounds(self, param_name: str) -> tuple[float, float]:
        left_bound = -np.inf
        right_bound = np.inf
        pm = self.pydantic_model
        if not pm or param_name not in pm.model_fields:
            return (left_bound, right_bound)
        metadata = pm.model_fields[param_name].metadata
        for rule in metadata:
            if isinstance(rule, Gt):
                left_bound = math.nextafter(rule.gt, np.inf)  # type: ignore
            elif isinstance(rule, Ge):
                left_bound = rule.ge
            elif isinstance(rule, Lt):
                right_bound = math.nextafter(rule.lt, -np.inf)  # type: ignore
            elif isinstance(rule, Le):
                right_bound = rule.le
        return (left_bound, right_bound)  # type: ignore

    def make_start_vector(self, param_names: list[str], bounds: list[tuple[float, float]] | None = None) -> list[float]:
        if not bounds:
            bounds = self.make_optimization_bounds(param_names)
        vector = []
        for index, p in enumerate(param_names):
            bound = None
            if bounds:
                bound = bounds[index]
            vector.append(self._get_start_value(p, bound))
        return vector

    def make_optimization_bounds(self, param_names: list[str]) -> list[tuple[float, float]]:
        bounds = []
        for p in param_names:
            bounds.append(self._make_optimization_bounds(p))
        return bounds

    @classmethod
    def wrap(cls, model) -> Self:
        if isinstance(model, type(cls)):
            return model
        return cls(model)


@dataclass
class ModelBinding:
    model: ModelWrapper
    defaults: dict[str, Any] = field(default_factory=dict)
