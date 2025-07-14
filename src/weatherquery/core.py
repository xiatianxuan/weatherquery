from .getapi import GetApi
from dataclasses import dataclass


@dataclass
class CityInfo:
    city: str
    citykey: str
    parent: str
    updateTime: str


@dataclass
class DayWeather:
    date: str
    high: str
    low: str
    ymd: str  # 日期
    week: str  # 星期几
    sunrise: str  # 日出时间
    sunset: str  # 日落时间
    aqi: int  # 空气指数
    fx: str  # 风向
    fl: str  # 风力
    wtype: str  # 天气（多云，晴 之类的文本）
    notice: str  # 温馨提示


@dataclass
class WeatherData:
    shidu: str  # 湿度，百分数字符串
    pm25: int
    pm10: int
    quality: str  # 空气质量
    wendu: str
    ganmao: str
    forecast: list[DayWeather]  # 未来天气预测
    yesterday: DayWeather  # 昨日天气


@dataclass
class MainData:
    cityInfo: CityInfo
    data: WeatherData


class Querier:
    def __init__(self, city_name):
        self._data = GetApi.get_city_weather_dict(city_name=city_name)
        self._data_data=self._data["data"]
        self._main_data = MainData(cityInfo=self.cityInfo, data=self.weatherData)

    @property
    def cityInfo(self) -> CityInfo:
        return CityInfo(**self._data["cityInfo"])

    @property
    def weatherData(self) -> WeatherData:
        return WeatherData(
            shidu=self._data_data["shidu"],
            pm25=self._data_data["pm25"],
            pm10=self._data_data["pm10"],
            quality=self._data_data["quality"],
            wendu=self._data_data["wendu"],
            ganmao=self._data_data["ganmao"],
            forecast=self.forecast,
            yesterday=self.yesterday,
        )

    @property
    def forecast(self):
        return (
            [
                DayWeather(
                    date=day["date"],
                    high=day["high"],
                    low=day["low"],
                    ymd=day["ymd"],
                    week=day["week"],
                    sunrise=day["sunrise"],
                    sunset=day["sunset"],
                    aqi=day["aqi"],
                    fx=day["fx"],
                    fl=day["fl"],
                    wtype=day["type"],  # 把 "type" 映射到 "wtype"
                    notice=day["notice"],
                )
                for day in self._data_data["forecast"]
            ],
        )

    @property
    def yesterday(self):
        return DayWeather(
            date=self._data_data["yesterday"]["date"],
            high=self._data_data["yesterday"]["high"],
            low=self._data_data["yesterday"]["low"],
            ymd=self._data_data["yesterday"]["ymd"],
            week=self._data_data["yesterday"]["week"],
            sunrise=self._data_data["yesterday"]["sunrise"],
            sunset=self._data_data["yesterday"]["sunset"],
            aqi=self._data_data["yesterday"]["aqi"],
            fx=self._data_data["yesterday"]["fx"],
            fl=self._data_data["yesterday"]["fl"],
            wtype=self._data_data["yesterday"]["type"],  # 把 "type" 映射到 "wtype"
            notice=self._data_data["yesterday"]["notice"],
        )

    @property
    def mainData(self):
        return self._main_data
