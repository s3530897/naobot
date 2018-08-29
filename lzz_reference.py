# -*- coding: utf-8 -*-
import urllib2,json
import requests
import re

#乐长长接口，登记用户需要记录的食物
url = 'http://119.29.248.56/nlp/api/v1.0/lzz_reference'

#获取食物信息
def lzz_reference(msg):
    msg=msg.encode("utf-8")


    message = {'gender': 'F','age':1,'wheght': 20}
    res = requests.post(url,data=message)
    result = res.json()
    print(result)


#连接天气模组
def connect_lzz_food_recognize(msg):
    flag = 0
    s = u''
    while (
            flag < 3):
        flag += 1
        try:
            s = lzz_reference(msg)
            break
        except Exception:
            s = u"网络连接错误"
            print(s)
    return s

if (
         __name__ == "__main__"):
    s=lzz_reference(u"查询营养素，小男孩，4岁，15公斤")