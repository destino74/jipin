# coding=utf-8
import logging
import re
import urllib
import urlparse
import setting
import sys
import os

from operator import itemgetter
from lxml import etree

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../core")))
import spider

class ZLSpider(spider.BasicSpider):
    sid = 3
    list_urls = [
        "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%B9%BF%E5%B7%9E&kw=python&sm=0&sg=00903cc1fd0d47998c6543e49ef201e7&p=1"
    ]
    index_wait_time = 3
    domain = "http://sou.zhaopin.com/"

    def build_index_request(self, url):
        return self.session.get(url, headers=setting.Headers)

    def build_detail_request(self, url):
        return self.build_index_request(url)

    def parse_index(self, response):
        html = response.content
        root = etree.HTML(html)
        info_list = root.xpath('//table[@class="newlist"]/tr/td')
        if not info_list:
            logging.info('[已到末页]')
            return

        detail_urls = root.xpath('//table[@class="newlist"]/tr/td/div/a/@href')
        for url in detail_urls:
            self.detail_queue.put(url)

        list_urls = root.xpath('//div[@class="pagesDown"]/ul/li/a/@href')
        # 解析列表页
        for url in list_urls:
            if not re.match(r"(https|http).*", url):
                url = urlparse.urljoin(self.domain, url)

            # >> 解析参数再重组,防止参数顺序不同的相同URL重复请求
            urlp = urlparse.urlparse(url)
            params = urlparse.parse_qs(urlp.query)
            query = [(key, value[0]) for key, value in params.iteritems()]
            query = sorted(query, key=itemgetter(0))
            data = urlp.scheme, urlp.netloc, urlp.path, urlp.params, urllib.urlencode(query), urlp.fragment
            url = urlparse.urlunparse(data)
            # <<

            if re.match(r"http://sou.zhaopin.com/jobs/searchresult.ashx(.*)", url) and url not in self.list_urls:
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
        ret['title'] = root.xpath("//div[@class='top-fixed-box']/div[@class='fixed-inner-box']/div/h1/text()")[0].encode('utf8')
        ret['content'] = ""
        ct_list = root.xpath("//div[@class='tab-cont-box']/div[1]/p")
        for ct in ct_list:
            ret['content'] += ct.xpath('string(.)') + '\n'
        ret['salary'] = extract_first(root.xpath("//ul[@class='terminal-ul clearfix']/li[1]/strong/text()")).strip().encode('utf8')
        ret['province'] = extract_first(root.xpath("//ul[@class='terminal-ul clearfix']/li[2]/strong/a/text()")).encode('utf8')
        ret['address'] = extract_first(root.xpath("//div[@class='tab-cont-box']/div[1]/h2/text()")).encode('utf8')
        ret['experience'] = extract_first(root.xpath("//ul[@class='terminal-ul clearfix']/li[5]/strong/text()")).encode('utf8')
        ret['education'] = extract_first(root.xpath("//ul[@class='terminal-ul clearfix']/li[6]/strong/text()")).encode('utf8')
        ret['company'] = extract_first(root.xpath("//p[@class='company-name-t']/a/text()"))
        ret['icon'] = extract_first(root.xpath("//div[@class='company-box']/p/a/img/@src"))
        ret['detail_id'] = re.findall("com/(.*).htm", url)[0]
        ret['url'] = url
        ret['source_id'] = self.sid

        return ret

    def extract_did(self, url):
        group = re.findall("com/(.*).htm", url)
        if len(group) != 0:
            did = group[0]
            return did
        else:
            raise Exception("提取detail id失败:%s" % url)

if __name__ == '__main__':
    logfile = os.path.join(os.path.dirname(__file__), "../log/zlzhaopin.log")

    ZLSpider("", "python", logfile).start()
