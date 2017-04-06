# coding:utf-8

__author__ = 'cmustard'

"""
使用代理模式访问网站
"""

import sys
import urllib2
import re


def testArgument():
    """
    测试输入参数，只需要一个参数
    :return:
    """
    if len(sys.argv) != 2:
        print(u'只需要一个参数就够了')
        tipUse()
        exit()
    else:
        TP = TestProxy(sys.argv[1])


def tipUse():
    """
    显示提示信息
    :return:
    """
    print(u'该程序只能输入一个参数，这个参数必须是一个可用的proxy')
    print(u'usage: python testUrllib2WithProxy.py http://1.2.3.4"5')
    print(u'usage: python testUrllib2WithProxy.py https://1.2.3.4:5')


class TestProxy(object):
    def __init__(self, proxy):
        self.proxy = proxy
        self.checkProxyFormat(self.proxy)
        self.url = 'http://www.google.com'
        self.timeout = 5
        self.flagWord = u'google'
        self.useProxy(self.proxy)

    def checkProxyFormat(self, proxy):
        try:
            proxyMatch = re.compile(r'''http[s]?://[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}:[\d]{1,5}$''')
            re.search(proxyMatch, proxy).group()
        except AttributeError:
            tipUse()
            exit()

        flag = 1
        proxy = proxy.replace('//', '')  # 去掉//
        try:
            protocol = proxy.split(':')[0]  # http
            # print protocol
            ip = proxy.split(':')[1]  # 192.168.1.183
            port = proxy.split(':')[2]  # 8080

        except IndexError:
            print(u'下标出界')
            tipUse()
            exit()
        flag = flag and len(proxy.split(':')) == 3 and len(ip.split('.')) == 4

        flag = ip.split('.')[0] in map(str, range(1, 256)) and flag
        flag = ip.split('.')[1] in map(str, range(1, 256)) and flag
        flag = ip.split('.')[2] in map(str, range(1, 256)) and flag
        flag = ip.split('.')[3] in map(str, range(1, 256)) and flag

        flag = protocol in [u'http', u'https'] and flag

        flag = port in map(str, xrange(1, 65536)) and flag

        '''检查是在proxy的格式'''

        if flag:
            print(u'输入的http代理服务器符合标准')
        else:
            tipUse()
            exit()

    def useProxy(self, proxy):
        """
        利用代理访问百度，并查找关键词
        :param proxy:
        :return:
        """
        protocol = proxy.split('//')[0].replace(':', '')
        ip = proxy.split('//')[1]

        opener = urllib2.build_opener(urllib2.ProxyHandler(proxies={protocol: ip}))
        urllib2.install_opener(opener)

        try:
            resp = urllib2.urlopen(self.url, timeout=self.timeout)
        except Exception as e:
            print(u'链接错误 {}，退出程序'.format(e))
            exit()

        else:
            str = resp.read()
            if re.search(self.flagWord, str):
                print(u'已经取得特征詞，该代理可用')
            else:
                print(u'该代理不可用')


if __name__ == '__main__':
    testArgument()
