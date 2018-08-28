# -*- coding: utf-8 -*
import ro_to_xf_to_ro as ro
import time

#基于本机中枢传递的人机交互测试
def interact():
    while(True):
        print('开始')
        localtime = time.localtime(time.time())
        print "本地时间为 :", localtime
        result=ro.integration_from_nao()
        ro.str_sclassification(result)
        print('中止')
        localtime = time.localtime(time.time())
        print "本地时间为 :", localtime
        time.sleep(6)
        print('终止')
        localtime = time.localtime(time.time())
        print "本地时间为 :", localtime

if (
        __name__ == "__main__"):
    interact()