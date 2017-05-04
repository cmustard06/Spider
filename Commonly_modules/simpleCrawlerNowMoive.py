#!/usr/bin/env python
# coding:utf-8

__author__ = 'cmustard'
"""
简单爬取影城影片信息
"""

import re
import urllib2
import json

class TodayMovie(object):
    def __init__(self):
        self.url="http://www.jycinema.com/frontUIWebapp/appserver/commonItemSkuService/findItemSku"
        self.timeout = 6
        self.fileName = './todayMovie.txt'
        '''内部变量定义完毕'''


    def getMovieInfo(self,cinId):
        data='''params={"cinemaId":"%s","showtime":"2017-04-26","type":"queryItemSku","memberLevelName":"","memberId":"","channelCode":"J0002","channelId":"3"}'''%(cinId)
        request = urllib2.Request(self.url,data=data,origin_req_host="www.jycinema.com")
        request.add_header('User-Agent',': Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0')
        request.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
        request.add_header('Cookie','zlgx.id=d4510077-0256-4b34-bf32-72b5765a50cfzlgxpt.id=15e80fee34934f2496bd7a3b8b098be3; zlgx.id=f2f5a19b-2241-4012-90f3-68693b82e16c')

        response = urllib2.urlopen(request)
        api = response.read()
        api_dict = json.loads(api)
        api_list = api_dict.get('data')
        if len(api_list) == 0:
            return False
        for index in range(len(api_list)):
            return api_list[index].get('address1'),api_list[index].get('filmName'),api_list[index].get('showtimeFormat')



if __name__ == '__main__':
    t = TodayMovie()
    print("[***]Start...")
    for cinId in range(400,600):

        if not t.getMovieInfo(cinId):
            continue
        else:
            for i in t.getMovieInfo(cinId):
                print i,
            print