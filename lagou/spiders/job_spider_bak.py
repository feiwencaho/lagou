import scrapy
import json


class JobSpider(scrapy.spiders.Spider):
    name = "jobsss"
    allowed_domains = ["lagou.com"]

    def start_requests(self):
        reqs = []
        cookies = {
            'JSESSIONID': 'JSESSIONID=ABAAABAAAFCAAEG1E0E56F4F90DDC04834B122A7445582F;',
            'SEARCH_ID': '2eed6dabfb1647c3894e4df4e7eda68a'
        }
        for i in range(2, 3):
            req = scrapy.Request(
                'https://www.lagou.com/zhaopin/Python/{page}/?filterOption={page}'.format(**{'page': i}),
                method='GET',
                cookies=cookies
            )
            reqs.append(req)
        return reqs

    def parse(self, response):
        li = response.xpath('//*[@id="s_position_list"]/ul/li')
        self.logger.info(len(li))
        for li_item in li:
            li_item.xpath('')
