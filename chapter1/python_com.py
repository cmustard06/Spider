# coding:utf-8

__author__ = 'cmustard'

import datetime
import urllib
import urlparse
import re
from threading import Thread
from Queue import Queue
import time

root_url = 'http://localhost.com:3000'
urls = Queue()
links = set()  # 总集合


def fetch(urls):
    """
    抓取页面链接
    :return:
    """
    global links

    while True:
        if urls.empty():
            urls.task_done()
            break

        url = urls.get()
        try:
            html = urllib.urlopen(url)

            print("[==>]{} -->{}  {}".format(datetime.datetime.ctime(datetime.datetime.now()), html.getcode(), url))
            html = html.read()
        except Exception as e:
            print("[!!!]{} \r\n appear error {}".format(e,url))
            continue
        pattern = re.compile(r'''href=["']?([^\s"'<>]+)''')
        origin_links = re.findall(pattern, html)

        # 存储抓取到的URL
        #
        if origin_links is None :
            continue
        else:
            partlinks = set()
            for link in origin_links:
                if not link.startswith('.') and not link.startswith('#'):
                    partlinks.add(link)
                    # print partlink
                    continue
            for link in partlinks.difference(links):

                if not link.startswith('http:') and not link.startswith('https:'):
                    url = urlparse.urljoin(root_url, link)

                    # 去除url中的frag
                    url = urlparse.urldefrag(url)[0]
                    urls.put(url)

                else:
                    urlparser = urlparse.urlparse(link)
                    if urlparser.netloc in "http://localhost.com:3000":
                        link = urlparse.urldefrag(link)[0]
                        urls.put(link)

                    else:
                        continue
                links.add(link)

    return links

def run():
    global urls
    urls.put(root_url)
    return fetch(urls)

if __name__ == '__main__':
    start = time.time()
    links = run()
    print("[***] FINISH!!! spend time {}s total {} url".format(time.time()-start,len(links)))
