from .getapi import GetApi
from .consts import LOGGER


def debug():
    # LOGGER.debug(get_api_by_citycode("101020100"))
    # LOGGER.debug(get_citycode_from_cityname("芜湖市"))
    LOGGER.debug(GetApi.get_city_weather_dict("芜湖市"))
