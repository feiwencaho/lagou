# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import uuid
from lagou.items import JobItem
from scrapy.shell import inspect_response


class JobSpider(CrawlSpider):
    name = 'job'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin/Python/']
    rules = (
        Rule(LinkExtractor(allow=("zhaopin/Python/*",)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        job = JobItem()
        job['name'] = response.xpath('//div[@class="job-name"]/span[@class="name"]/text()').extract_first()
        job['company'] = response.xpath('//div[@class="job-name"]/div[@class="company"]/text()').extract_first()
        job['salary'] = response.xpath('//dd[@class="job_request"]/p[1]/span[1]/text()').extract_first()
        job['city'] = response.xpath('//dd[@class="job_request"]/p[1]/span[2]/text()').extract_first()[1:-1].strip()
        job['experience'] = response.xpath(
            '//dd[@class="job_request"]/p[1]/span[3]/text()').extract_first()[:-1].strip()
        job['education'] = response.xpath('//dd[@class="job_request"]/p[1]/span[4]/text()').extract_first()[:-1].strip()
        job['nature'] = response.xpath('//dd[@class="job_request"]/p[1]/span[5]/text()').extract_first()
        duty_p = response.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()').extract()
        duty = '\n'.join(duty_p)
        job['duty'] = duty
        job['address'] = ''.join(response.xpath('//div[@class="work_addr"]/a[position()<3]/text()').extract())
        if job['name'] is None:
            inspect_response(response, self)
        job['url'] = response.url
        self.logger.info(job)
        return job
