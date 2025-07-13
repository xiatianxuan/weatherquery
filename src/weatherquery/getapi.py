# -*- coding: utf-8 -*-
import urllib.request
import json
from . import utils


@utils.get_time
def getapi(city_code:str)->dict:
    url = f'https://www.weather.com.cn/data/sk/{city_code}.html'

    # 构造请求头，防止 301/302
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )

    # 发送请求，拿到原始字节
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read()          # bytes

    # 手动解码(经实验，此api编码为 utf-8)
    text = raw.decode('utf-8', errors='ignore')
    data = json.loads(text)

    return data

if __name__=="__main__":
    print(getapi("101010100"))