# coding=utf-8
import logging
import re
import urllib
import urlparse
import setting
import sys
import os
from lxml import etree

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../core")))
import spider


class ZLSpider(spider.BasicSpider):
    sid = 4
    list_urls = [
        "http://search.51job.com/list/030200,000000,0000,00,9,99,python,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
    ]
    index_wait_time = 10
    domain = "http://search.51job.com"
    log_file_name = "51job.log"

    def build_index_request(self, url):
        return self.session.get(url, headers=setting.HEADERS)

    def build_detail_request(self, url):
        return self.session.get(url, headers=setting.HEADERS)

    def parse_index(self, response):
        html = response.content
        root = etree.HTML(html)

        # 取详情页列表
        detail_urls = root.xpath("//div[@id='resultList']/div[@class='el']/p/span/a/@href")
        if not detail_urls:
            logging.info('[已到末页]')
            return

        for url in detail_urls:
            self.detail_queue.put(url)

        list_urls = root.xpath("//div[@class='dw_page']/div/div/div/ul/li/a/@href")
        # 取列表页列表
        for url in list_urls:
            if not re.match(r"(https|http).*", url):
                url = urlparse.urljoin(self.domain, url)

            # >> 解析参数再重组,目的防止参数顺序不同的相同URL重复请求
            urlp = urlparse.urlparse(url)
            params = urlparse.parse_qs(urlp.query)
            query = [(key, value[0]) for key, value in params.items()]
            data = urlp.scheme, urlp.netloc, urlp.path, urlp.params, urllib.urlencode(query), urlp.fragment
            url = urlparse.urlunparse(data)
            # <<
            if re.match(r"http://search.51job.com/list/(.*)", url) and url not in self.list_urls:
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
        ret['title'] = extract_first(root.xpath("//div[@class='tHeader tHjob']/div/div/h1/text()")).encode('utf8')
        ret['content'] = "\n".join(root.xpath("//div[@class='bmsg job_msg inbox']/text()")).strip().encode('utf8')
        ret['salary'] = extract_first(root.xpath("//div[@class='tHeader tHjob']/div/div/strong/text()")).encode('utf8')
        ret['province'] = extract_first(root.xpath("//div[@class='tHeader tHjob']/div/div/span/text()")).encode('utf8')
        ret['address'] = "\n".join(root.xpath("//div[@class='bmsg inbox']/p/text()")).strip().encode('utf8')
        ret['experience'] = extract_first(root.xpath("//div[@class='jtag inbox']/div/span/text()")).encode('utf8')
        ret['education'] = ""
        ret['company'] = extract_first(root.xpath("//div[@class='tHeader tHjob']/div/div/p/a/text()")).encode('utf8')
        ret['icon'] = ""
        ret['detail_id'] = re.findall("/(.*).html", url)[0]
        ret['url'] = url
        ret['source_id'] = self.sid

        return ret

    def extract_did(self, url):
        group = re.findall("/(.*).html", url)
        if len(group) != 0:
            did = group[0]
            return did
        else:
            raise Exception("[提取detail id失败] url:%s" % url)

if __name__ == '__main__':
    logfile = os.path.join(os.path.dirname(__file__), "../log/51job.log")
    ZLSpider("", "python", logfile).start()
