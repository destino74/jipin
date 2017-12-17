# coding=utf-8

import re
import sys
import time
import traceback
import gevent
import requests
import logging
import os

from gevent import monkey
from Queue import Queue
from filter import DummyFilter
from pipeline import RedisPipeline
from log import setup_logger
monkey.patch_all()


class BasicSpider(object):
    list_urls = []            # 起始列表页
    index_wait_time = 20      # 列表页请求间隔,秒
    detail_wait_time = 1      # 详情页请求间隔,秒
    log_file_name = ""

    def __init__(self, city, keyword, logfile=""):
        self.session = requests.session()
        self.session.keep_alive = False
        self.detail_queue = Queue()
        self.query = {
            "city": city,
            "province": "",
            "keyword": keyword
        }
        self.pipeline = RedisPipeline()
        self.filter = DummyFilter(self.sid)
        self.statistics = {
            'cur_page': 0,
            'finished': 0,
            'failed': 0,
            'total': 0,
        }
        if not logfile:
            logfile = os.path.join(os.path.dirname(__file__), "../log/%s.log" % self.sid)

        self.logger = setup_logger(logfile)

    @property
    def sid(self):
        """
        平台ID, 1-lagou, 2-liepin, 3-智联招聘, 4-前程无忧
        :return:
        """
        raise NotImplemented

    def build_index_request(self, url):
        """
        构建列表页请求
        :param url:
        :return: index response
        """
        raise NotImplemented

    def build_detail_request(self, url):
        """
        构建详情页请求
        :param url:
        :return: detail response
        """
        raise NotImplemented

    def parse_index(self, response):
        """
        解析列表页, 获取内容页链接
        :param response:
        :return:
        """
        raise NotImplementedError

    def parse_detail(self, response, url):
        """
        解析列表页, 获取内容页链接
        :param response:
        :return: dict of detail
        """
        raise NotImplemented

    def start(self):
        """

        """
        try:
            g1 = gevent.spawn(self.get_index)
            time.sleep(5)
            g2 = gevent.spawn(self.get_detail)
            g1.join()
            self.detail_queue.join()
        except KeyboardInterrupt:
            print 'KeyboardInterrupt'
            sys.exit(0)

    def get_index(self):
        """
        解析列表页
        :return:
        """
        for url in self.list_urls:
            resp = self.build_index_request(url)
            if resp.status_code == 200:
                logging.info("[解析列表页] url: %s" % url)
                self.parse_index(resp)
                time.sleep(self.index_wait_time)
            else:
                self.logger.error('[请求列表页错误] url: %s code: %s' % (url, resp.status_code))

    def get_detail(self):
        """
        解析详情页
        :return:
        """
        while True:
            # 从任务队列取数据
            url = self.detail_queue.get()
            try:
                did = self.extract_did(url)
            except Exception as e:
                self.logger.error('[Exception] %s' % e.message)
                # traceback.print_exc()
            else:
                if not self.check_exist(did):
                    try:
                        resp = self.build_detail_request(url)
                    except Exception:
                        traceback.print_exc()
                        time.sleep(3)
                    else:
                        if resp.status_code == 200:
                            try:
                                data = self.parse_detail(resp, url)
                            except:
                                traceback.print_exc()
                                self.logger.error("[解析详情页错误] url: %s" % url)
                            else:
                                self.pipeline.save_data(data)
                                self.logger.info("[解析详情页] url: %s" % url)
                        else:
                            self.logger.error("[请求详情页错误] url: %s, code: %s"  % (resp.status_code, url))
                        time.sleep(self.detail_wait_time)
                else:
                    self.logger.info("[详情页排重] url: %s" % url)
            finally:
                # 任务队列减1
                self.detail_queue.task_done()

    def extract_did(self, url):
        """
        提取detail id
        :param url: detail url
        :return: detail id
        """
        group = re.findall(r"/(\d+).shtml", url)
        if len(group) != 0:
            did = group[0]
            return did
        else:
            raise Exception("[提取detail id失败] url:%s" % url)

    def check_exist(self, did):
        """
        判断detail是否存在
        :param did:
        :return: bool
        """
        return self.filter.exist(did)

