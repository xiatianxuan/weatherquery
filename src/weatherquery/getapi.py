# -*- coding: utf-8 -*-
from . import consts
import urllib.request
import json
from . import utils


class GetApi:
    """
    api请求工具包
    """

    @staticmethod
    @utils.get_time
    def get_api_by_citycode(city_code: str) -> dict:
        """
        根据城市编码请求城市天气信息字典
        """
        # url = f'https://www.weather.com.cn/data/sk/{city_code}.html'
        url = f"http://t.weather.itboy.net/api/weather/city/{city_code}"

        utils.LOGGER.debug(f"Getting Api with citycode: {city_code}, url is {url}")

        # 构造请求头，防止 301/302
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )

        # 发送请求，拿到原始字节
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()  # bytes

        # 手动解码(经实验，此api编码为 utf-8)
        text = raw.decode("utf-8", errors="ignore")
        data = json.loads(text)

        return data

    @staticmethod
    @utils.get_time
    def get_citycode_from_cityname(name: str) -> str:
        """
        根据城市名获取城市编码
        """
        with open(consts.CITIES_FILE_PATH) as f:
            city_code = [i for i in json.load(f) if i["city_name"] == name][0][
                "city_code"
            ]
        return city_code

    @staticmethod
    @utils.get_time
    def get_city_weather_dict(city_name: str) -> dict:
        code = GetApi.get_citycode_from_cityname(city_name)
        return GetApi.get_api_by_citycode(code)
    



if __name__ == "__main__":
    print(get_api_by_citycode("101010100"))
