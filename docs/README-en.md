# WeatherQuery
> A lightweight and convenient weather query Python library

[中文](../README.md) / English

## Installation
Install directly using pip:
```bash
pip install git+https://gitee.com/xiatianxuan/weatherquery.git
```

## Usage
1. Import the Library
```py
import weatherquery as wq
```
2. Create a Query Object
```py
q = wq.Querier("Beijing")  # Replace "Beijing" with the name of the city you want to query
```
3. Query the Weather
```py
print(q.today)  # to print today's weather
```
> For more query functions, please refer to the src/weatherquery/core.py file.

## Declaration
The API used in this project is provided by http://t.weather.itboy.net/api/weather/city/. It is for personal technical use only and is not allowed for commercial use or misuse. Any negative impacts resulting from misuse of this project are not related to this project!