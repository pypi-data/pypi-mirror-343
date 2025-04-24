# This is an auto-generated file. Do not change it manually
#
# fmt: off
from ..resource_type_helpers import ResourceTypeDescriptor
from typing import Annotated, Optional, Literal


class pvgis_seriescalc_table(ResourceTypeDescriptor):
    

    standard = ResourceTypeDescriptor.make_attrs(
        resource_type='pvgis_seriescalc_table',
    )

    def __init__(
        self,
        *,
        datasource: Annotated[Optional[Literal['pvgis']], "data source"] = None,
        pvgis_database: Optional[Literal['PVGIS-SARAH', 'PVGIS-ERA5']] = None,
    ):
        self._instance_attrs = ResourceTypeDescriptor.make_attrs(
            resource_type='pvgis_seriescalc_table',
            datasource=datasource,
            pvgis_database=pvgis_database,
        )
