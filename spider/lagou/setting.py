# coding=utf-8
# 请求json的url
API_URL = "https://www.lagou.com/jobs/positionAjax.json"

# 爬取职位要求的url
INFO_URL = "https://www.lagou.com/jobs/%s.html"

# 请求json文件用的headers
INDEX_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88?px=default&city=%E6%B7%B1%E5%9C%B3&district=%E5%8D%97%E5%B1%B1%E5%8C%BA",
    "X-Requested-With": "XMLHttpRequest",
    "Host": "www.lagou.com",
    "Connection": "keep-alive",
    "Origin": "https://www.lagou.com",
    "Upgrade-Insecure-Requests": "1",
    "X-Anit-Forge-Code": "0",
    "X-Anit-Forge-Token": "None",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8"
}

# 爬取职位要求的header
DETAIL_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    "Cookie": "_gat=1; user_trace_token=20171106132303-8eb9c16c-7e38-47c8-8d9d-db3ae62fe298; LGUID=20171106132309-93b59e5f-c2b2-11e7-97af-5254005c3644; JSESSIONID=ABAAABAAAFCAAEG31B17D21C4DB97DC024DEBD94CD14B6A; _putrc=4A8DBAB174C19F48; login=true; unick=%E6%A2%81%E9%94%A6%E5%B3%B0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=7; PRE_UTM=; PRE_HOST=www.google.com; PRE_SITE=https%3A%2F%2Fwww.google.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F2404939.templates; SEARCH_ID=bce490fbf05c4268aa00f6472d26e5df; index_location_city=%E5%B9%BF%E5%B7%9E; TG-TRACK-CODE=search_code; _gid=GA1.2.1045063910.1512194672; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512194672,1512220657,1512221036,1512221166; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512221258; _ga=GA1.2.560901708.1509945817; LGSID=20171202211652-0feaf917-d763-11e7-9ba6-5254005c3644; LGRID=20171202212653-76089e6a-d764-11e7-9ba6-5254005c3644; user_trace_token=20171106132303-8eb9c16c-7e38-47c8-8d9d-db3ae62fe298; LGUID=20171106132309-93b59e5f-c2b2-11e7-97af-5254005c3644; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=7; index_location_city=%E5%B9%BF%E5%B7%9E; login=false; unick=""; _putrc=""; JSESSIONID=ABAAABAAAFCAAEG31B17D21C4DB97DC024DEBD94CD14B6A; TG-TRACK-CODE=index_navigation; SEARCH_ID=581f35b8668a4e8eaa4ce08bf71d56b9; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F2974823.templates; X_HTTP_TOKEN=fe6a80f102af04bce5de732e2be6f28c; _gid=GA1.2.1045063910.1512194672; _ga=GA1.2.560901708.1509945817; LGSID=20171203013240-cbe4f179-d786-11e7-9bb6-5254005c3644; LGRID=20171203015748-4e78e9bd-d78a-11e7-bda3-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512194672,1512220657,1512221036,1512221166; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512237513"
}



