#!/usr/bin/env python
# coding:utf-8

__author__ = 'cmustard'

import logging
import getpass
import sys

# 自定义MyLog类
class MyLog(object):
    '''这个类用于创建一个自用的log'''
    def __init__(self): # 类MyLog的构造函数
        user = getpass.getuser()  # 获取登陆的用户名
        self.logger = logging.getLogger(user)  #日志处理器的name 为user
        self.logger.setLevel(logging.DEBUG)  # 设置全局日志级别
        logFile = './'+sys.argv[0][0:-3]+'.log'
        # print logFile
        formatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s',datefmt='%Y-%m-%d %H:%M:%S')

        '''日志显示到屏幕上并输出到日志文件内'''
        logHand = logging.FileHandler(logFile)
        logHand.setFormatter(formatter)
        logHand.setLevel(logging.ERROR)  # 设置处理器的日志级别


        logHandSt = logging.StreamHandler()
        logHandSt.setFormatter(formatter)

        self.logger.addHandler(logHand)
        self.logger.addHandler(logHandSt)

    '''日志的5个级别对应以下的5个函数'''
    def debug(self,msg):
        self.logger.debug(msg)

    def info(self,msg):
        self.logger.info(msg)

    def warn(self,msg):
        self.logger.warning(msg)

    def error(self,msg):
        self.logger.error(msg)

    def critical(self,msg):
        self.logger.critical(msg)


if __name__ == '__main__':
    mylog = MyLog()
    mylog.debug("i'm debug")
    mylog.info("i'm info")
    mylog.warn("i'm warn")
    mylog.error("i'm error")
    mylog.critical("i'm critical")