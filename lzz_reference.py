# -*- coding: utf-8 -*-
import urllib2,json
import requests
import re

#乐长长接口，登记用户需要记录的食物
url = 'http://119.29.248.56/nlp/api/v1.0/lzz_parse'

#获取食物信息
def lzz_reference(msg):
    msg=msg.encode("utf-8")

    s = u'好的，记录'

    message = {'msg':msg}
    res = requests.post(url,data=message)
    result = res.json()
    result_food=result['food_info']
    #食物种类
    for index in range(0,len(result_food)):
        if(index>0):
            s += u'，'
        if(result_food[index][u'sub_properties']):
            if(result_food[index][u'sub_properties'][u'quantity']<1):
                s += str(result_food[index][u'sub_properties'][u'quantity']) +result_food[index][u'sub_properties'][u'unit']+ \
                     result_food[index][u'properties'][u'cal_name']+ u'，共计'+str(int(result_food[index][u'sub_properties'][u'grams'])) + u'克'
            else:
                s += str(int(result_food[index][u'sub_properties'][u'quantity'])) + result_food[index][u'sub_properties'][u'unit'] + \
                     result_food[index][u'properties'][u'cal_name']+ u'，共计'+str(int(result_food[index][u'sub_properties'][u'grams'])) + u'克'
        else:
            s += result_food[index][u'properties'][u'cal_name']
    s += u'。您今天总共摄入了膳食营养素,'
    #食物营养
    result_basic=result['nutritions']["basic"]
    for index in range(0,len(result_basic)):
        s += result_basic[index]['name']+str(round(result_basic[index]['value'],2))
        if(result_basic[index]['unit']==u'g'):
            s += u'克，'
        else:
            s += u'卡，'
    s += u'摄入了维生素,'
    result_vitamin = result['nutritions']["vitamin"]
    for index in range(0,len(result_vitamin)):
        s += result_vitamin[index]['name'] + u',' + str(round(result_vitamin[index]['value'],2))
        if(result_vitamin[index]['unit'] == u'ug'):
            s += u'微克，'
        else:
            s += u'毫克，'
    s += u'摄入了矿物质营养元素,'
    result_trace_element = result['nutritions']["trace_element"]
    for index in range(0,len(result_trace_element)):
        s += result_trace_element[index]['name'] + str(round(result_trace_element[index]['value'],2))
        if(result_trace_element[index]['unit'] == u'ug'):
            s += u'微克，'
        else:
            s += u'毫克，'
    result_others = result['nutritions']["others"]
    s += u'摄入了,'
    result_others = result['nutritions']["others"]
    for index in range(0, len(result_others)):
        s += result_others[index]['name'] + u',' + str(round(result_others[index]['value'], 2))
        if (result_others[index]['unit'] == u'ug'):
            s += u'微克，'
        elif(result_others[index]['unit'] == u'mg'):
            s += u'毫克，'
        elif (result_others[index]['unit'] == u'g'):
            s += u'克，'
        elif (result_others[index]['unit'] == u'mmol'):
            s += u'摩尔，'
        else:
            pass
    print(s)
    return s


#连接天气模组
def connect_lzz_reference(msg):
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
    s=connect_lzz_reference(u"吃了一碗饭，两瓶可乐，吃了土豆牛肉")
    print(s)