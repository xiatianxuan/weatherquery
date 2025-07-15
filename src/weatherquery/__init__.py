from .assets import emm

assert emm==0, "assets没有被正确安装"


from .getapi import GetApi
from .core import *
from .consts import LOGGER


def debug():
    # LOGGER.debug(get_api_by_citycode("101020100"))
    # LOGGER.debug(get_citycode_from_cityname("芜湖市"))
    # LOGGER.debug(GetApi.get_city_weather_dict("芜湖"))
    q = Querier("北京市")
    LOGGER.debug(q.forecast)
    LOGGER.debug(q.cityInfo)
    # LOGGER.debug(q.mainData)

    q = Querier("呼和浩特")
    LOGGER.debug(q.today)
    LOGGER.debug(q.cityInfo)
    # LOGGER.debug(q.mainData)
