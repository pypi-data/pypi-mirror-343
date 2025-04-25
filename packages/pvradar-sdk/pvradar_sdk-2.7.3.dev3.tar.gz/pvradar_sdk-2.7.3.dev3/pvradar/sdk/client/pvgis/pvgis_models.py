from typing import Any, Annotated as A, Optional
import pandas as pd
from pydantic import Field

from ...common.exceptions import DataUnavailableError
from .pvgis_client import PvgisClient, PvgisSeriescalcParams, PvgisDatabase, pvgis_csv_to_pandas
from ...common.pandas_utils import crop_by_interval
from pvlib.location import Location
from ...modeling.decorators import datasource, standard_resource_type
from ...modeling.utils import auto_attr_table
from ...modeling import R
from ..pvradar_resources import SeriesAttrs, SeriesConfigAttrs as S
from ...modeling.resource_types._list import standard_mapping


pvgis_series_name_mapping: dict[str, str | A[Any, SeriesAttrs]] = {
    'G(i)': A[pd.Series, S(resource_type='global_horizontal_irradiance', unit='W/m^2', agg='mean', freq='1h')],
    'H_sun': A[pd.Series, S(resource_type='solar_elevation_angle', unit='deg', agg='mean', freq='1h')],
    'T2m': A[pd.Series, S(resource_type='air_temperature', unit='degC', agg='mean', freq='1h')],
    'WS10m': A[pd.Series, S(resource_type='wind_speed', unit='m/s', agg='mean', freq='1h')],
}


def _auto_attr_table(df: pd.DataFrame, **kwargs) -> None:
    if df is None:
        return
    auto_attr_table(
        df,
        series_name_mapping=pvgis_series_name_mapping,
        resource_annotations=standard_mapping,
        **kwargs,
    )
    for name in df:
        df[name].attrs['datasource'] = 'pvgis'


# ----------------------------------------------------
# PVGIS tables


@standard_resource_type(R.pvgis_seriescalc_table)
@datasource('pvgis')
def pvgis_seriescalc_table(
    *,
    location: A[Location, Field()],
    interval: A[pd.Interval, Field()],
    pvgis_database: Optional[PvgisDatabase] = None,
    tz: Optional[str] = None,
) -> pd.DataFrame:
    do_bfill = False
    query: PvgisSeriescalcParams = {
        'lon': location.longitude,
        'lat': location.latitude,
        'startyear': interval.left.tz_convert('utc').year,
        'endyear': interval.right.tz_convert('utc').year,
    }

    if query['startyear'] < 2005:
        if interval.left > pd.Timestamp('2005-01-01T00:00:00+05:00'):
            do_bfill = True
            query['startyear'] = 2005
        else:
            raise ValueError('PVRADAR does not provide PVGISdata prior to 2004-12-31 20:00:00 UTC')
    if pvgis_database is not None:
        query['raddatabase'] = pvgis_database
    response = PvgisClient.instance().get_seriescalc(query)
    result = pvgis_csv_to_pandas(response, tz=tz if tz is not None else location.tz)
    returned_pvgis_database = result.attrs.get('pvgis_database')
    result = crop_by_interval(result, interval)
    if not len(result):
        raise DataUnavailableError(interval=interval, where='PVGIS seriescalc tool')

    # this is a hack to make year 2005 available in European time zones
    # by backfilling a few hours prior to 2005-01-01 00:00:00 UTC
    if do_bfill and len(result):
        index = pd.date_range(interval.left, result.index[-1], freq='h')
        original = result
        result = result.reindex(index)
        result = result.bfill()
        # workaround for bug in pandas overwriting attrs
        for column in result.columns:
            result[column].attrs = original[column].attrs

    _auto_attr_table(result)
    if returned_pvgis_database is not None:
        result.attrs['pvgis_database'] = returned_pvgis_database
        for name in result:
            result[name].attrs['pvgis_database'] = returned_pvgis_database
    return result


# ----------------------------------------------------
# PVGIS series (alphabetical order)


@standard_resource_type(R.air_temperature)
@datasource('pvgis')
def pvgis_air_temperature(
    *,
    pvgis_seriescalc_table: A[pd.DataFrame, R.pvgis_seriescalc_table],
    pvgis_database: Optional[PvgisDatabase] = None,
) -> pd.Series:
    return pvgis_seriescalc_table['T2m']


@standard_resource_type(R.global_horizontal_irradiance)
@datasource('pvgis')
def pvgis_global_horizontal_irradiance(
    *,
    pvgis_seriescalc_table: A[pd.DataFrame, R.pvgis_seriescalc_table],
    pvgis_database: Optional[PvgisDatabase] = None,
) -> pd.Series:
    return pvgis_seriescalc_table['G(i)']


@standard_resource_type(R.solar_elevation_angle)
@datasource('pvgis')
def pvgis_solar_elevation_angle(
    *,
    pvgis_seriescalc_table: A[pd.DataFrame, R.pvgis_seriescalc_table],
    pvgis_database: Optional[PvgisDatabase] = None,
) -> pd.Series:
    return pvgis_seriescalc_table['H_sun']


@standard_resource_type(R.wind_speed)
@datasource('pvgis')
def pvgis_wind_speed(
    *,
    pvgis_seriescalc_table: A[pd.DataFrame, R.pvgis_seriescalc_table],
    pvgis_database: Optional[PvgisDatabase] = None,
) -> pd.Series:
    return pvgis_seriescalc_table['WS10m']
