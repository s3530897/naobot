# -*- coding: utf-8 -*-
import urllib2,json
import requests
import re

#乐长长接口，登记用户需要记录的食物
url = 'http://119.29.248.56/nlp/api/v1.0/food_detect'

#获取食物信息
def lzz_food_recognize(msg):
    msg=msg.encode("utf-8")
    message = {'msg':msg}
    res = requests.post(url,json=message)
    result = res.json()
    s=u'好的，记录'
    for index in range(0,len(result)):
        if(index>0):
            s += u'，'
        if(result[index][u'sub_properties']):
            if(result[index][u'sub_properties'][u'quantity']<1):
                s += str(result[index][u'sub_properties'][u'quantity']) +result[index][u'sub_properties'][u'unit']+\
                    result[index][u'properties'][u'cal_name']+ u'，共计'+str(int(result[index][u'sub_properties'][u'grams'])) + u'克'
            else:
                s += str(int(result[index][u'sub_properties'][u'quantity'])) + result[index][u'sub_properties'][u'unit'] +\
                    result[index][u'properties'][u'cal_name']+ u'，共计'+str(int(result[index][u'sub_properties'][u'grams'])) + u'克'
        else:
            s += result[index][u'properties'][u'cal_name']

    return s


#连接天气模组
def connect_lzz_food_recognize(msg):
    flag = 0
    s = u''
    while (
            flag < 3):
        flag += 1
        try:
            s = lzz_food_recognize(msg)
            break
        except Exception:
            s = u"网络连接错误"
            print(s)
    return s

if (
         __name__ == "__main__"):
    s=connect_lzz_food_recognize(u"记录我喝了两瓶可乐一瓶矿泉水还有一碗土豆牛肉")
    print(s)