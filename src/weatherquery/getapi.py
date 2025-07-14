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
            city_code = [i for i in json.load(f) if GetApi._is_the_same_city(name,i["city_name"])][0][
                "city_code"
            ]
        return city_code

    @staticmethod
    @utils.get_time
    def get_city_weather_dict(city_name: str) -> dict:
        code = GetApi.get_citycode_from_cityname(city_name)
        return GetApi.get_api_by_citycode(code)
    
    @staticmethod
    def _is_the_same_city(user_cityname:str,file_cityname:str):
        """
        比较两个城市是否为同一城市
        Args: 
        user_cityname: 用户指定的城市
        file_cityname: 文件里存储的城市

        此函数为了确保 (芜湖市 芜湖) (安徽省 安徽) 之类的城市可以被识别成同一个
        """
        uc=user_cityname

        ignore_list=['省','市','区','县',"村","乡","旗","自治区","直辖市","特别行政区"]
        for ig in ignore_list:
            # 去掉结尾的行政区级别
            if uc.endswith(ig):
                uc=uc[:-len(ig)]
                break
        
        return file_cityname.startswith(uc)

        




if __name__ == "__main__":
    print(get_api_by_citycode("101010100"))
