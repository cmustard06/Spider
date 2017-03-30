# coding:utf-8

__author__ = 'cmustard'

"""
多线程爬虫爬取python官方文档
"""
from Queue import Queue
from threading import Thread, Lock
import urlparse
import socket
import re
import time

seen_urls = set(['/'])
lock = Lock()


class Fetcher(Thread):

    def __init__(self, tasks):
        # Thread.__init__(self)
        super(Fetcher, self).__init__()
        self.tasks = tasks
        self.daemon = True

        self.start()

    def run(self):
        while True:
            url = self.tasks.get()
            print("[==>] {}".format("http://localhost.com:3000"+url))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost.com', 3000))
            get = 'GET {} HTTP/1.0\r\nHost:localhost.com:3000\r\n\r\n'.format(url)
            sock.send(get)
            response = ''
            chunk = sock.recv(4096)
            while chunk:
                response += chunk
                chunk = sock.recv(4096)

            links = self.parse_links(url, response)

            lock.acquire()
            for link in links.difference(seen_urls): # 属于links但是不属于seen_urls,即新的url
                self.tasks.put(link)
            seen_urls.update(links)  # 列表就用update
            lock.release()
            self.tasks.task_done()

    def parse_links(self, fetched_url, response):
        if not response:
            print('error:{}'.format(fetched_url))
            return set()
        if not self._is_html(response):
            return set()
        urls = re.findall(r'''href=["']?([^\s"'<>]+)''', self.body(response))

        links = set()
        for url in urls:
            normalized = urlparse.urljoin(fetched_url, url)
            parts = urlparse.urlparse(normalized)
            if parts.scheme not in ('', 'http', 'https'):
                continue
            host, port = parts.hostname, parts.port
            if host and host.lower() not in ('localhost'):
                continue
            # 除去frag，即#号后面的字符串
            defragmented, frag = urlparse.urldefrag(parts.path)
            links.add(defragmented)

        return links

    def body(self, response):
        body = response.split('\r\n\r\n')[1]
        return body

    def _is_html(self, response):
        head, body = response.split('\r\n\r\n')
        headers = dict([head.split(': ') for head in head.split('\r\n')][1:])

        return 'text/html' in headers.get('Content-Type')


class ThreadPool(object):
    def __init__(self, num_threads):
        self.tasks = Queue()
        for _ in range(num_threads):
            Fetcher(self.tasks)

    def add_task(self, url):
        self.tasks.put(url)

    def wait_completion(self):
        self.tasks.join()

if __name__ == '__main__':
    start = time.time()
    pool = ThreadPool(4)
    pool.add_task("/")
    pool.wait_completion()
    print('{} URLs fetched in {:.1f} seconds'.format(len(seen_urls), time.time()-start))
