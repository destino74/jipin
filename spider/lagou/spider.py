# coding=utf-8
import json
import re
import time
import setting
import urllib3.contrib.pyopenssl
import os
import sys

from gevent import monkey
from lxml import etree

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../core")))
import spider

monkey.patch_all()
urllib3.contrib.pyopenssl.inject_into_urllib3()


class LagouSpider(spider.BasicSpider):
    sid = 1
    index_wait_time = 20
    detail_wait_time = 1

    # 初始化数据，传入城市和关键词
    def __init__(self, city, keyword, logfile):
        super(LagouSpider, self).__init__(city, keyword, logfile)
        # 构建查询字符串参数
        self.params = {
            "needAddtionalResult": False,
            "isSchoolJob": 0
        }
        # 如果没有 city 字段默认查询全国的职位，有则加上相应城市
        if city != '全国':
            self.params['city'] = city
        self.list_urls = ["https://www.lagou.com/jobs/positionAjax.json"]
        self.page = 1
        self.info_wait_time = 20

    def build_detail_url(self, data, num):
        for i in range(num):
            position_id = data['content']['positionResult']['result'][i]['positionId']
            url = setting.INFO_URL % position_id
            self.detail_queue.put(url)

    def build_detail_request(self, url):
        resp = self.session.get(url, headers=setting.DETAIL_HEADER)
        return resp

    def build_index_request(self, url):
        resp = self.session.post(url=url, params=self.params, headers=setting.INDEX_HEADER, data={
            "first": "false",
            "pn": self.page,
            "kd": self.query.get('keyword', '')
        })
        self.page += 1
        return resp

    def parse_index(self, response):
        # 把得到的json数据转成字典
        data = json.loads(response.text)
        # 此处可能遇到API的5次/min限制, 避让重试
        if 'success' in data and not data['success']:
            time.sleep(10)
        else:
            num = data['content']['positionResult']['resultSize']
            total_count = data['content']['positionResult']['totalCount']
            self.statistics['finished'] += num
            self.statistics['total'] = total_count

            # 构建url
            self.build_detail_url(data, num)
            if self.statistics['finished'] >= total_count:
                return
            self.list_urls.append(setting.API_URL)

    def extract_did(self, url):
        group = re.findall(r"/jobs/(\d+)", url)
        if len(group) != 0:
            did = group[0]
            return did
        else:
            raise Exception("提取detail id失败:%s" % url)

    def parse_detail(self, response, url):
        def extract_first(l):
            if not l:
                return ""
            else:
                return l[0]

        root = etree.HTML(response.text)
        ret = {}
        ret['title'] = extract_first(root.xpath("//div[@class='job-name']/span/text()")).encode('utf8')
        ret['content'] = root.xpath("//dd[@class='job_bt']")[0].xpath('string(.)').encode('utf8')
        ret['salary'] = root.xpath("//span[@class='salary']")[0].xpath('string(.)').encode('utf8')
        ret['province'] = extract_first(root.xpath("//div[@class='work_addr']/a[1]/text()")).encode('utf8')
        ret['address'] = "-".join(root.xpath("//div[@class='work_addr']/a[not(@id='mapPreview')]/text()")).encode(
            'utf8')
        ret['address'] += "-" + "".join(root.xpath("//div[@class='work_addr']/text()")).encode('utf8'). \
            replace('-', ' ').strip()
        ret['experience'] = extract_first(root.xpath("//dd[@class='job_request']/p/span[2]/text()")).encode('utf8'). \
            replace('/', '').strip()
        ret['education'] = extract_first(root.xpath("//dd[@class='job_request']/p/span[3]/text()")).encode('utf8'). \
            replace('/', '').strip()
        ret['url'] = url
        ret['company'] = extract_first(root.xpath("//div[@class='work_addr']/a[1]/text()")).encode('utf8')
        ret['icon'] = extract_first(root.xpath("//dl[@class='job_company']/dt/a/img/@src")).encode('utf8')
        ret['source_id'] = 1
        ret['detail_id'] = re.findall("/jobs/(\d+).html", url)[0]
        return ret


if __name__ == '__main__':
    logfile = os.path.join(os.path.dirname(__file__), "../log/lagou.log")
    spider = LagouSpider("广州", "python", logfile)
    spider.start()
