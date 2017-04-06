# coding:utf-8

__author__ = 'cmustard'

"""
测试使用urllib2模块
"""


import urllib2
import time
import platform
import os


def clear():
    """
    该函数用于清屏
    :return:
    """
    print(u"内容过多，显示3s后翻页")
    time.sleep(3)
    OS = platform.system()
    if OS == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def linkBaidu():
    url = 'https://www.baidu.com'

    try:
        resp = urllib2.urlopen(url, timeout=2)
    except urllib2.URLError:
        print(u'网络地址错误')
        exit()
    else:
        with open('./baidu.txt', 'w') as f:
            f.write(resp.read())

    print(u'获取URL信息，resp.geturl() \n: {}'.format(resp.geturl()))
    print(u'获取返回代码,resp.getcode()\n: {}'.format(resp.getcode()))
    print(u'获取返回信息,resp.info()\n: {}'.format(resp.info()))
    print(u'获取的网页内容已经存入当前目录的baidu.txt中，请自行打开！！')

if __name__ == '__main__':
    linkBaidu()