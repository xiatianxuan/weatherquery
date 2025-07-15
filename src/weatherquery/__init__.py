from .assets import emm

assert emm==0, "assets没有被正确安装"


from .getapi import GetApi
from .core import *
from .consts import LOGGER


def debug():
    q = Querier("北京市")
    LOGGER.debug(q.forecast)
    LOGGER.debug(q.cityInfo)
    q = Querier("呼和浩特")
    LOGGER.debug(q.today)
    LOGGER.debug(q.cityInfo)