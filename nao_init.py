# -*- coding: utf-8 -*
import file_transport as ft

#nao机器人初始化设定
def init_main():
    ft.transit_to_r("E:/work/CNLP/resource/what.wav","/home/nao/what.wav")

if (
        __name__ == "__main__"):
    init_main()