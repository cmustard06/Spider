#!/usr/bin/env python
# coding:utf-8

__author__ = 'cmustard'
'''
用于测试代理是否可用
'''
import urllib2
import re
import sys
import urlparse

def tipUse():
    """
    帮助文档
    :return:
    """
    print(u'该程序只能输入一个参数，这个参数必须是一个可用的proxy')
    print(u'python testUrllib2WithProxy.py http://1.2.3.4:8080')
    print(u'python testUrllib2WithProxy.py https://1.2.3.4:9999')

def testArgs():
    """
    参数验证
    :return:
    """
    if len(sys.argv)!=2:
        print(u'只需要一个参数就够了！！！')
        tipUse()
        return False
    else:
        return True

class TestProxy(object):
    """
    主程序，测试代理是否可用
    """
    def __init__(self, proxy):
        self.proxy = proxy
        self.url = 'http://www.google.com'
        self.flagWord = u'google'
        self.timeout = 100
        self.testProxy()

    def checkProxy(self):
        """
        检查代理服务地址的格式是否正确
        :return:
        """
        # 是否是正确的代理地址
        proxyMatch = re.compile(r'http[s]?://[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}:[\d]{1,5}$')
        try:
            re.search(proxyMatch, self.proxy).group()
        except AttributeError as e:
            # print(e)
            tipUse()
            exit()
        part = urlparse.urlparse(self.proxy)
        schema = part.scheme
        self.host = part.hostname
        self.port = part.port
        if schema not in (u'http', u'https'):
            print(u'协议错误')
            tipUse()
            exit()
        else:
            self.flag = True
        # 开始判断ip地址是否正确
        ipList = self.host.split('.')
        # print ipList
        for num in ipList:
            self.flag = int(num)<256 and int(num)>=0 and self.flag

        # 最后检查
        if not self.flag:
            print(u'ip地址范围问题')
            tipUse()
            return False
        else:
            return True

    def testProxy(self):
        """
        测试代理
        :return:
        """
        if not self.checkProxy():
            exit()

        opener = urllib2.build_opener(urllib2.ProxyHandler({self.host:self.port}))
        urllib2.install_opener(opener)
        try:
            resp = urllib2.urlopen(self.url,timeout=self.timeout)
        except urllib2.URLError:
            print(u'URL连接失败，请重试')
            tipUse()
            exit()
        else:
            if self.flagWord in resp.read():
                print(u'连接成功，获取到特征词，该代理不可用')
            else:
                print(u'该代理不可用')

if __name__ == '__main__':
    if testArgs():
        TestProxy(sys.argv[1])
    else:
        exit()