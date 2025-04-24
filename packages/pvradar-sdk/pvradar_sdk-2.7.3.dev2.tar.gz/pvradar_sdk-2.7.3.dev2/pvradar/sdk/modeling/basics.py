import copy
import inspect
from dataclasses import dataclass, field
from types import NoneType
from typing import (
    Any,
    Callable,
    Literal,
    Mapping,
    NotRequired,
    Optional,
    Self,
    Type,
    TypeGuard,
    TypeVar,
    TypedDict,
    get_args,
    override,
)

from .resource_types._list import PvradarResourceType, Datasource

AggFunctionName = Literal[
    'sum',
    'mean',
    'std',
    'min',
    'max',
    'count',
    'first',
    'last',
    'median',
]

DataType = Literal[
    'any',
    'float',
    'int',
    'string',
    'datetime',  # normally pd.Timestamp
    'unix_timestamp',
    'sweep_range',
    'table',
    'series',
    'array',
]


def is_pvradar_resource_type(value: Any) -> TypeGuard[PvradarResourceType]:
    return value in get_args(PvradarResourceType.__value__)


class BaseResourceAttrs(TypedDict):
    resource_type: NotRequired[str]


class ModelParamAttrs(BaseResourceAttrs):
    """Parameter attrs, also used in .resource() call"""

    to_unit: NotRequired[str]
    set_unit: NotRequired[str]
    to_freq: NotRequired[str]
    agg: NotRequired[AggFunctionName]

    measurement_id: NotRequired[str]
    source_id: NotRequired[str]

    keep: NotRequired[bool]

    params: NotRequired[Mapping[str, Any]]


class Attrs(ModelParamAttrs):
    """PVRADAR-specific attrs that use pvradar_resource_type unlike a generic resource_type"""

    resource_type: NotRequired[PvradarResourceType]  # type: ignore
    datasource: NotRequired[Datasource]


def attrs(
    *,
    to_unit: Optional[str] = None,
    set_unit: Optional[str] = None,
    to_freq: Optional[str] = None,
    agg: Optional[AggFunctionName] = None,
    measurement_id: Optional[str] = None,
    source_id: Optional[str] = None,
    keep: Optional[bool] = None,
    params: Optional[Mapping[str, Any]] = None,
    resource_type: Optional[PvradarResourceType] = None,
    datasource: Optional[Datasource] = None,
) -> Attrs:
    result: Attrs = {}
    if to_unit is not None:
        result['to_unit'] = to_unit
    if set_unit is not None:
        result['set_unit'] = set_unit
    if to_freq is not None:
        result['to_freq'] = to_freq
    if agg is not None:
        result['agg'] = agg
    if measurement_id is not None:
        result['measurement_id'] = measurement_id
    if source_id is not None:
        result['source_id'] = source_id
    if keep is not None:
        result['keep'] = keep
    if params is not None:
        result['params'] = params
    if resource_type is not None:
        result['resource_type'] = resource_type
    if datasource is not None:
        result['datasource'] = datasource
    return result  # type: ignore


class SeriesAttrs(BaseResourceAttrs):
    freq: NotRequired[str]
    unit: NotRequired[str]
    agg: NotRequired[AggFunctionName]


class FrameAttrs(BaseResourceAttrs):
    freq: NotRequired[str]


class ModelConfig(TypedDict):
    disable_validation: NotRequired[bool]  # e.g. validation of attrs in model params
    disable_auto_resolve: NotRequired[bool]  # if true then context['model_name'] will NOT be resolved as ModelBinding
    ignore_missing_params: NotRequired[bool]  # model will be executed (run) even if some params are missing


class ModelRecipe(TypedDict):
    model_name: str
    params: NotRequired[Mapping[str, Any]]
    label: NotRequired[str]


class BindingNotFound:
    def __init__(self, reason: str = '') -> None:
        self.reason = reason

    @classmethod
    def check(cls, subject: Any) -> bool:
        return subject is BindingNotFound or isinstance(subject, cls)


class EmptyBinding:
    """marker object for binding returning None"""


LambdaSubject = TypeVar('LambdaSubject')


class LambdaArgument:
    def __init__(self, type: Type[LambdaSubject], callable: Callable[[LambdaSubject], Any]):
        self.type = type
        self.callable = callable


@dataclass
class ModelParam:
    name: str = '_anonymous'
    annotation: Any = None
    attrs: Mapping[str, Any] = field(default_factory=dict)
    default: Optional[Any] = inspect.Parameter.empty
    type: Type = NoneType
    lambda_argument: Optional[LambdaArgument] = None

    @override
    def __repr__(self) -> str:
        result = str(self.annotation)
        if self.default != inspect.Parameter.empty:
            if result.endswith('>'):
                result = result[:-1]
            result += f' = {self.default}'
        if result.startswith('<') and not result.endswith('>'):
            result += '>'
        return result

    def copy(self) -> Self:
        return copy.copy(self)


@dataclass
class Audience:
    any_org: bool = False
    org_ids: list[str] = field(default_factory=list)
    project_goals: list[str] = field(default_factory=list)
