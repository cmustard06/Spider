# coding:utf-8

__author__ = 'cmustard'


import socket
import time
import re
import urlparse
import Queue
from threading import Thread, Lock


seen_urls = set(['/'])
lock = Lock()

class Fetcher(Thread):
    """
    页面抓取
    """
    def __init__(self, tasks):
        super(Fetcher, self).__init__()
        self.daemon = True  # 开启守护线程
        self.tasks = tasks

        self.start()

    def run(self):
        while True:
            url = self.tasks.get()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost.com', 3000))
            get = '''GET {} HTTP/1.0\r\nHost: localhost.com:3000\r\n\r\n'''.format(url)
            sock.send(get)
            response = ''
            chunk = sock.recv(4096)
            while chunk:
                response +=chunk
                chunk = sock.recv(4096)
            # 分析链接地址
            links = self.parse_link(url, response)

            # 判断链接是否已经被爬取
            lock.acquire()
            for link in links.difference(seen_urls):
                self.tasks.put(link)
            seen_urls.update(links)
            lock.release()
            self.tasks.task_done()

    def parse_link(self, fetched_link, response):
        """
        :param fetched_link:
        :param response:
        :return: 分析完成后的链接集合
        """
        if not response:
            print("[!!!]error url: {}".format(fetched_link))
            return set()

        is_html, code = self._is_html(response)
        print("[==>] {} {} {}".format(time.asctime(), code, 'http://localhost.com:3000'+fetched_link))
        if not is_html:
            return set()

        urls = re.findall(r'''href=["']?([^\s"'<>]+)''', self.get_body(response))
        links = set()

        # 开始分析获取到的url是否是所需要的
        for url in urls:
            url = urlparse.urljoin(fetched_link, url)
            urlp = urlparse.urlparse(url)
            if urlp.scheme not in ('', 'http', 'https'):
                continue
            host, port = urlp.hostname, urlp.port
            if host and host.lower() not in ('localhost.com'):
                continue
            # 除去#后的frag
            # print url
            defrag, frag = urlparse.urldefrag(url)
            links.add(defrag)
        return links

    def _is_html(self, response):
        """
        判断抓取到的内容是否是text/html
        :param response:
        :return: boolean,code
        """
        header, body = response.split('\r\n\r\n')
        headers = dict([head.split(': ') for head in header.split('\r\n')][1:])
        code = header.split('\r\n')[0]
        return ('text/html' in headers.get('Content-Type'), code)

    def get_body(self, response):
        """
        获取服务器返回内容中的html部分
        :param response:
        :return: body
        """
        body = response.split("\r\n\r\n")[1]
        return body


class ThreadPool(object):
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.tasks = Queue.Queue()
        for _ in range(self.num_threads):
            Fetcher(self.tasks)

    def add_task(self, task):
        self.tasks.put(task)

    def wait_completion(self):
        self.tasks.join()  # 阻塞直到队列中所有项目都已经被得到和处理


def run():
    start = time.time()
    th = ThreadPool(4)
    th.add_task('/')
    th.wait_completion()
    print("[***] Finish !!! speed time {:.2f}s, total collect {} urls".format(time.time()-start, len(seen_urls)))


if __name__ == '__main__':
    print("[***] Start crawling  pages!!!")
    run()
