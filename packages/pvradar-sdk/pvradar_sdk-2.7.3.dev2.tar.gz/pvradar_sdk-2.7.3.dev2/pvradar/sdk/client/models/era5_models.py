from typing import Any, Annotated as A, Literal, Optional

import pandas as pd
from pvlib.location import Location

from ...common.exceptions import ApiException, DataUnavailableError
from ..api_query import Query
from ..client import PvradarClient
from ..pvradar_resources import SeriesConfigAttrs as S
from ...modeling import resource_types as R
from ...modeling.basics import Attrs as P
from ...modeling.decorators import datasource, standard_resource_type
from ...modeling.model_context import ModelContext
from ...modeling.resource_types._list import standard_mapping
from ...modeling.utils import auto_attr_table, convert_series_unit

era5_series_name_mapping: dict[str, str | A[Any, Any]] = {
    # ----------------------------------------------------
    # Single levels
    #
    '2m_temperature': A[pd.Series, S(resource_type='air_temperature', unit='degK', agg='mean', freq='1h')],
    'snow_depth': A[
        pd.Series, S(resource_type='snow_depth_water_equivalent', unit='m', agg='mean', freq='1h')
    ],  # snow_depth_water
    'snowfall': A[pd.Series, S(resource_type='snowfall_water_equivalent', unit='m', agg='sum', freq='1h')],  # snowfall_water
    'snow_density': A[pd.Series, S(resource_type='snow_density', unit='kg/m^3', agg='mean', freq='1h')],
    # ----------------------------------------------------
    # Pressure levels
    'relative_humidity': A[pd.Series, S(resource_type='relative_humidity', unit='%', agg='mean', freq='1h')],
}


def _auto_attr_table(df: pd.DataFrame, **kwargs) -> None:
    if df is None:
        return
    auto_attr_table(
        df,
        series_name_mapping=era5_series_name_mapping,
        resource_annotations=standard_mapping,
        **kwargs,
    )
    for name in df:
        df[name].attrs['datasource'] = 'era5'


# ----------------------------------------------------
# ERA5 tables


@standard_resource_type(R.era5_single_level_table)
@datasource('era5')
def era5_single_level_table(
    location: Location,
    interval: pd.Interval,
) -> pd.DataFrame:
    query = Query.from_site_environment(location=location, interval=interval)
    query.set_path('datasources/era5/raw/hourly/csv')
    result = PvradarClient.instance().get_df(query, crop_interval=interval)

    if not len(result):
        raise DataUnavailableError(interval=interval, where='era5 global dataset')

    _auto_attr_table(result)

    if (
        len(result)
        and interval.left > pd.Timestamp('2005-01-01T00:00:00+05:00')
        and interval.left <= pd.Timestamp('2005-01-01T00:00:00UTC')
    ):
        index = pd.date_range(interval.left, result.index[-1], freq='h')
        original = result
        result = result.reindex(index)
        result = result.bfill()
        # workaround for bug in pandas overwriting attrs
        for column in result.columns:
            result[column].attrs = original[column].attrs

    return result


# ----------------------------------------------------
# ERA5 series (alphabetical order)
def make_land_series(
    *,
    location: Location,
    interval: pd.Interval,
    resource_type_name: str,
    unit: Optional[str],
) -> pd.Series:
    query = Query.from_site_environment(location=location, interval=interval)
    query['sensors'] = resource_type_name
    query['dataset_name'] = 'era5-land'
    query.set_path('datasources/era5/data')
    try:
        result = PvradarClient.instance().get_df(query, crop_interval=interval)[resource_type_name]
        result.attrs['dataset_name'] = 'era5-land'
        if unit is not None:
            result.attrs['unit'] = unit
        return result
    except ApiException as e:
        if e.status_code == 422 and 'not available' in str(e):
            raise DataUnavailableError(str(e)) from e
        raise e


Era5DatasetName = Literal[
    'era5-land',
    'era5-global',
    # 'era5-single-levels', 'era5-pressure-levels'
]


@standard_resource_type(R.total_precipitation)
@datasource('era5')
def era5_total_precipitation(
    location: Location,
    interval: pd.Interval,
    dataset_name: Era5DatasetName = 'era5-land',  # nothing in era5-global
) -> pd.Series:
    return make_land_series(
        location=location,
        interval=interval,
        resource_type_name='total_precipitation',
        unit='m',
    )


@standard_resource_type(R.rainfall)
@datasource('era5')
def era5_rainfall(
    location: Location,
    interval: pd.Interval,
    total_precipitation: A[pd.Series, R.total_precipitation(datasource='era5')],
    dataset_name: Era5DatasetName = 'era5-land',  # nothing in era5-global
) -> pd.Series:
    return total_precipitation


@standard_resource_type(R.global_horizontal_irradiance)
@datasource('era5')
def era5_global_horizontal_irradiance(
    location: Location,
    interval: pd.Interval,
    dataset_name: Era5DatasetName = 'era5-land',  # nothing in era5-global
) -> pd.Series:
    return make_land_series(
        location=location,
        interval=interval,
        resource_type_name='global_horizontal_irradiance',
        # TODO: check what is the right unit, or maybe this is another resource_type, e.g. R.surface_downwelling_shortwave_flux_in_air
        # Official standard_name: surface_downwelling_shortwave_flux_in_air
        # Official long_name: Surface short-wave (solar) radiation downwards
        # Official unit: J/m^2
        # maybe W/m^2 is more appropriate, so it may require division by 60 or 3600 or 86400 or so
        unit='J/m^2',
    )


@standard_resource_type(R.air_temperature)
@datasource('era5')
def era5_air_temperature(
    *,
    location: Location,
    interval: pd.Interval,
    context: ModelContext,
    dataset_name: Era5DatasetName = 'era5-global',
) -> pd.Series:
    if dataset_name == 'era5-land':
        return make_land_series(
            location=location,
            interval=interval,
            resource_type_name='air_temperature',
            unit='degK',
        )
    else:
        era5_single_level_table = context.resource(R.era5_single_level_table)
        assert era5_single_level_table is not None
        return convert_series_unit(era5_single_level_table['2m_temperature'], to_unit='degC')


@standard_resource_type(R.relative_humidity)
@datasource('era5')
def era5_relative_humidity(
    *,
    era5_single_level_table: A[pd.DataFrame, P(resource_type='era5_single_level_table')],
) -> pd.Series:
    series = era5_single_level_table['relative_humidity']
    if series.attrs['unit'] != '%':
        raise ValueError(f'Unexpected unit: {series.attrs["unit"]}')
    return series.copy()


@standard_resource_type(R.snow_density)
@datasource('era5')
def era5_snow_density(
    *,
    location: Location,
    interval: pd.Interval,
    context: ModelContext,
    dataset_name: Era5DatasetName = 'era5-global',
) -> pd.Series:
    if dataset_name == 'era5-land':
        return make_land_series(
            location=location,
            interval=interval,
            resource_type_name='snow_density',
            unit='kg/m^3',
        )
    else:
        era5_single_level_table = context.resource(R.era5_single_level_table)
        assert era5_single_level_table is not None
        return era5_single_level_table['snow_density'].copy()


@standard_resource_type(R.snow_depth_water_equivalent)
@datasource('era5')
def era5_snow_depth_water_equivalent(
    *,
    location: Location,
    interval: pd.Interval,
    context: Any,
    dataset_name: Era5DatasetName = 'era5-global',
) -> pd.Series:
    if dataset_name == 'era5-land':
        return make_land_series(
            location=location,
            interval=interval,
            resource_type_name='snow_depth_water_equivalent',
            unit='m',
        )
    else:
        era5_single_level_table = context.resource(R.era5_single_level_table)
        assert era5_single_level_table is not None
        return era5_single_level_table['snow_depth'].copy()


@standard_resource_type(R.snow_depth)
@datasource('era5')
def era5_snow_depth(
    *,
    location: Location,
    interval: pd.Interval,
    context: ModelContext,
    dataset_name: Era5DatasetName = 'era5-global',
) -> pd.Series:
    if dataset_name == 'era5-land':
        return make_land_series(
            location=location,
            interval=interval,
            resource_type_name='snow_depth',
            unit='m',
        )
    elif dataset_name == 'era5-global':
        water_density = 1000
        snow_density = context.resource(R.snow_density, datasource='era5')
        assert snow_density is not None
        era5_snow_depth_water_equivalent = context.resource(R.snow_depth_water_equivalent, datasource='era5')
        assert era5_snow_depth_water_equivalent is not None
        return era5_snow_depth_water_equivalent * (water_density / snow_density)
    else:
        raise ValueError(f'Unknown dataset_name: {dataset_name}')


@standard_resource_type(R.snowfall_water_equivalent)
@datasource('era5')
def era5_snowfall_water_equivalent(
    *,
    location: Location,
    interval: pd.Interval,
    context: ModelContext,
    dataset_name: Era5DatasetName = 'era5-global',
) -> pd.Series:
    if dataset_name == 'era5-land':
        return make_land_series(
            location=location,
            interval=interval,
            resource_type_name='snowfall_water_equivalent',
            unit='m',
        )
    else:
        era5_single_level_table = context.resource(R.era5_single_level_table)
        assert era5_single_level_table is not None
        return era5_single_level_table['snowfall']


@standard_resource_type(R.snowfall)
@datasource('era5')
def era5_snowfall(
    *,
    era5_snowfall_water_equivalent: A[pd.Series, P(resource_type='snowfall_water_equivalent', datasource='era5')],
) -> pd.Series:
    snow_density_value = 100  # Kg/m^3, value for fresh snow
    water_density = 1000
    result = era5_snowfall_water_equivalent * (water_density / snow_density_value)
    result.attrs['agg'] = 'sum'
    return result


@standard_resource_type(R.wind_speed)
@datasource('era5')
def era5_wind_speed(
    *,
    location: Location,
    interval: pd.Interval,
    dataset_name: Era5DatasetName = 'era5-land',  # nothing in era5-global
) -> pd.Series:
    u10m = make_land_series(
        location=location,
        interval=interval,
        resource_type_name='u10m_wind_component',
        unit='m/s',
    )
    v10m = make_land_series(
        location=location,
        interval=interval,
        resource_type_name='v10m_wind_component',
        unit='m/s',
    )
    result = (u10m**2 + v10m**2) ** 0.5
    return result
