#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-04 09:52:00
# @Author  : cmustard (cmustard06@gmail.com)
# @Link    : http://www.cmustard.com
# @Version : $Id$

"""
单线程爬取豆瓣小说信息
"""

import bs4
import urllib
import urllib2
import time
import random
import sys

from HTMLParser import HTMLParseError

length = 0
pcUserAgent = {
"safari 5.1 – MAC":"User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
"safari 5.1 – Windows":"User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
"IE 9.0":"User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
"IE 8.0":"User-Agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
"IE 7.0":"User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
"IE 6.0":"User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
"Firefox 4.0.1 – MAC":"User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Firefox 4.0.1 – Windows":"User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Opera 11.11 – MAC":"User-Agent: Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
"Opera 11.11 – Windows":"User-Agent: Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
"Chrome 17.0 – MAC":"User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
"Maxthon":"User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
"Tencent TT":"User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
"The World 2.x":"User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
"The World 3.x":"User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
"sogou 1.x":"User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
"360":"User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
"Avant":"User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
"Green Browser":"User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
}

def readHTML(tag, **params):
	"""
	获取网页内容,返回bs4.BeautifulSoup()对象
	"""
	# print params
	if not params:
		urlparam = urllib.urlencode(params)
	else:
		urlparam = ""
	# 对中文字符进行url编码
	tag = urllib.quote(tag.encode('utf8'))
	
	url = "http://book.douban.com/tag/"+tag
	
	try:
		request = urllib2.Request(url,urlparam)
		# 随机获取一个UA，将其转换成字典类型
		uc = []
		uc.append(tuple(random.choice(pcUserAgent.values()).split(": ")))
		# print uc
		request.add_header = dict(uc)
		time.sleep(0.5)
		response = urllib2.urlopen(request)
	except urllib2.URLError as e:
		print e
		sys.exit(1)
	except urllib2.HTTPError as e:
		print e
		sys.exit(1)
	except Exception as e:
		print e
		sys.exit(1)

	# 获取网页内容，并进行解析
	html = response.read()
	soup = bs4.BeautifulSoup(html,'html.parser')
	return soup

 
def parser(tag, soup):
	"""
	解析网页，并存储在文档，返回是否解析成功
	"""
	# soup = readHTML()
	global length
	# 判断是对抓取完成
	try:
		books = soup.body.find_all('li',{"class":"subject-item"})
	except HTMLParseErro as e:
		print e
		return False

	# 抓取目标并进行存储
	crawlerResult = {}
	for book in books:
		# print type(book)
		bookname = book.find_all('h2',{'class':""})[0].a.get_text().replace("\n","").replace(" ","")		
		author = book.find_all('div',{'class':'pub'})[0].get_text().replace("\n","").replace(" ","")
		crawlerResult[bookname] = []
		crawlerResult[bookname].append(author)
	filename = tag+str(time.strftime('%Y-%m-%d'))+'.txt'
	length += len(crawlerResult)
	# 获取目前抓取内容的长度

	print "[***] NOW Length:%s"%length
	with open(filename,"a") as f:
		for key in crawlerResult.keys():
			f.write(key.encode('utf8')+"\t\t"+crawlerResult[key][0].encode('utf8')+"\n\r")

	return True

def main():
	print("[***] Start......")
	# 从首页中获取标签，图书类型
	tagSoup = readHTML("")
	originTags = tagSoup.find_all("table",{"class":"tagCol"})
	tags = []
	for tag in originTags:
		tagPart = [tag.get_text() for tag in tag.find_all('a')]
		tags.extend(tagPart)
	
	# 开始抓取目标内容
	for tag in tags[:10]:
		while True:
			start = 0
			soup = readHTML(tag,start=start,type="T")
			result = parser(tag, soup)
			if not result:
				print("[!!!]Finished!!!")
				break
			else:
				start += 20
				continue
			
	
if __name__ == '__main__':

	main()
	
	

