#!/usr/bin/env python
# coding:utf-8

__author__ = 'cmustard'

"""
修改header中的userAgent，有时候可以返回不同的页面
"""

import urllib2
import userAgent

class Urllib2ModifyHeader(object):
    def __init__(self, url):
        self.url = url

    def useUserAgent(self, userAgent, name):
        request = urllib2.Request(self.url)
        userAgentHeader, userAgent = userAgent.split(':')
        request.add_header(userAgentHeader, userAgent)

        try:
            resp = urllib2.urlopen(request)
        except urllib2.URLError:
            print(u'url有错误！！请重试！！')
            exit()
        else:
            filename = str(name)+'.html'
            with open(filename, 'w+') as f:
                f.write('{}\r\n'.format(userAgent)+resp.read())

if __name__ == '__main__':
    url = 'http://fanyi.youdao.com'
    t = Urllib2ModifyHeader(url)
    PIUA = userAgent.pcUserAgent['IE 9.0']
    MUUA = userAgent.mobileUserAgent['UC standard']
    t.useUserAgent(PIUA, 1)  # 1是html文件的名字
    t.useUserAgent(MUUA, 2)  
