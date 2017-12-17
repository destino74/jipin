# coding=utf-8
import logging
import re
import urllib
import urlparse
import sys
import os
from lxml import etree

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../core")))
import spider


class LiePinSpider(spider.BasicSpider):
    sid = 2
    list_urls = [
        "https://www.liepin.com/zhaopin/?ckid=bfedc3717b4b70d5&dqs=050020&key=python&d_pageSize=40&d_&curPage=1"
    ]
    index_wait_time = 3
    domain = "https://www.liepin.com/"
    log_file_name = "lipin.log"

    def build_index_request(self, url):
        return self.session.get(url)

    def build_detail_request(self, url):
        return self.session.get(url)

    def parse_index(self, response):
        html = response.content
        root = etree.HTML(html)
        no_result = root.xpath('//div[@class="alert alert-info sojob-no-result-alert"]')
        if no_result:
            logging.info('[已到末页]')

        detail_urls = root.xpath('//div[@class="job-info"]/h3/a/@href')
        for url in detail_urls:
            if url.startswith('/a'):
                url = self.domain + url
            self.detail_queue.put(url)

        # 解析列表页
        list_urls = root.xpath('//div[@class="pagerbar"]/a/@href')
        for url in list_urls:

            if not re.match(r"(https|http).*", url):
                url = urlparse.urljoin(self.domain, url)
            urlp = urlparse.urlparse(url)
            params = urlparse.parse_qs(urlp.query)
            query = [(key, value[0]) for key, value in params.items()]
            data = urlp.scheme, urlp.netloc, urlp.path, urlp.params, urllib.urlencode(query), urlp.fragment
            url = urlparse.urlunparse(data)
            if re.match(r"https://www.liepin.com/(a|zhaopin)/.*", url) and url not in self.list_urls:
                self.list_urls.append(url)

    def parse_detail(self, response, url):
        def extract_first(l):
            if not l:
                return ""
            else:
                return l[0]

        html = response.content
        root = etree.HTML(html)
        ret = {}
        ret['title'] = root.xpath("//h1/text()")[0].encode('utf8')
        ret['content'] = "\n".join(root.xpath("//div[@class='content content-word']/text()")).encode('utf8')
        ret['salary'] = "".join(root.xpath("//p[@class='job-item-title']/text()")).strip().encode('utf8')
        ret['province'] = root.xpath("//p[@class='basic-infor']/span/text()")[0].encode('utf8')
        ret['address'] = extract_first(root.xpath("//div[@class='new-compwrap']/ul[1]/li[3]/text()")).encode('utf8')

        if re.findall("/job/(\d+)", url):
            ret['experience'] = extract_first(root.xpath("//div[@class='job-qualifications']/span[2]/text()")).encode('utf8')
            ret['education'] = extract_first(root.xpath("//div[@class='job-qualifications']/span[1]/text()")).encode('utf8')
            ret['company'] = extract_first(root.xpath("//div[@class='company-logo']/p/a/text()"))
            ret['icon'] = extract_first(root.xpath("//div[@class='company-logo']/a/img/@src"))
            ret['detail_id'] = re.findall("/job/(\d+).shtml", url)[0]
        elif re.findall("/a/(\d+)", url):
            ret['experience'] = extract_first(root.xpath("//div[@class='resume clearfix']/span[2]/text()")).encode('utf8')
            ret['education'] = extract_first(root.xpath("//div[@class='resume clearfix']/span[1]/text()")).encode('utf8')
            ret['company'] = extract_first(root.xpath("//p[@class='company-name']/text()")).encode('utf8')
            ret['detail_id'] = re.findall("/a/(\d+).shtml", url)[0]
            ret['icon'] = ""
        ret['url'] = url
        ret['source_id'] = self.sid

        return ret

    def extract_did(self, url):
        group = re.findall(r"/(\d+).shtml", url)
        if len(group) != 0:
            did = group[0]
            return did
        else:
            raise Exception("提取detail id失败:%s" % url)

if __name__ == '__main__':
    logfile = os.path.join(os.path.dirname(__file__), "../log/liepin.log")
    LiePinSpider("", "python", logfile).start()
