# This is an auto-generated file. Do not change it manually
#
# fmt: off
from ..resource_type_helpers import ResourceTypeDescriptor
from typing import Annotated, Optional, Literal


class global_horizontal_irradiance(ResourceTypeDescriptor):
    """The total solar irradiance received by a horizontal up-facing surface. """


    standard = ResourceTypeDescriptor.make_attrs(
        resource_type='global_horizontal_irradiance',
        to_unit='W/m^2',
        agg='mean',
    )

    def __init__(
        self,
        *,
        datasource: Annotated[Optional[Literal['pvgis']], "data source"] = None,
        to_unit: Annotated[Optional[str], 'convert to unit'] = None,
        set_unit: Annotated[Optional[str], 'override unit'] = None,
        to_freq: Annotated[Optional[str], 'resample result using new freq'] = None,
        pvgis_database: Optional[Literal['PVGIS-SARAH', 'PVGIS-ERA5']] = None,
    ):
        self._instance_attrs = ResourceTypeDescriptor.make_attrs(
            resource_type='global_horizontal_irradiance',
            datasource=datasource,
            to_unit=to_unit,
            set_unit=set_unit,
            to_freq=to_freq,
            pvgis_database=pvgis_database,
        )
