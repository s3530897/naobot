# -*- coding: utf-8 -*-
import urllib2,json
#调用和风天气的API city可以通过https://cdn.heweather.com/china-city-list.txt城市列表获取
url = 'https://free-api.heweather.com/v5/weather?city=CN101280601&key=8a439a7e0e034cdcb4122c918f55e5f3'

#天气模组
def weather():
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req).read()
    # print resp
    # print type(resp)
    #将JSON转化为Python的数据结构
    json_data = json.loads(resp)
    city_data=json_data['HeWeather5'][0]
    hourly_data= json_data['HeWeather5'][0]['hourly_forecast']
    daily_data = json_data['HeWeather5'][0]['daily_forecast']
    print json_data
    s = city_data['basic']['city'] + u'，PM指数' + city_data['aqi']['city']['pm25'] + u'，白天' + daily_data[0]['cond']['txt_d'] +\
        u'，夜间' + daily_data[0]['cond']['txt_n'] + u'，气温' + daily_data[0]['tmp']['min'] + u'度到' + daily_data[0]['tmp']['max'] +\
        u'度。' + json_data['HeWeather5'][0]['suggestion']['drsg']['txt']
    print(s)
    return s

#连接天气模组
def connect_weather():
    flag = 0
    s = u''
    while (
            flag < 3):
        flag += 1
        try:
            s = weather()
            break
        except Exception:
            s = u"网络连接错误"
            print(s)
    return s

if (
         __name__ == "__main__"):
    connect_weather()