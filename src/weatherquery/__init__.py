from .getapi import GetApi
from .core import *


def debug():
    from .consts import LOGGER

    # LOGGER.debug(get_api_by_citycode("101020100"))
    # LOGGER.debug(get_citycode_from_cityname("芜湖市"))
    # LOGGER.debug(GetApi.get_city_weather_dict("芜湖"))
    q=Querier("芜湖")
    LOGGER.debug(q.cityInfo)
    LOGGER.debug(q.mainData)
