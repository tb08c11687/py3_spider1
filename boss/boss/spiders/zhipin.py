# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BossItem

class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c100010000/?query=python&page=1']

    rules = (
        #职位列表匹配规则
        Rule(LinkExtractor(allow=r'.+\?query=python&page=\d'), follow=True),
        #职位详情匹配规则
        #https://www.zhipin.com/job_detail/415bd7ab904f60a91X1629q5FlM~.html
        Rule(LinkExtractor(allow=r'.+/job_detail/.+.html'),callback='parse_item',follow=False)
    )

    def parse_item(self, response):
        name = response.xpath("//div[@class='name']/h1/text()").get()
        salary = response.xpath("//div[@class='name']/span/text()").get().strip()
        info_primary = response.xpath("//div[@class='job-primary detail-box']/div[@class='info-primary']/p//text()").getall()
        city = info_primary[0].split("：")[1]
        experience = info_primary[1].split("：")[1]
        education = info_primary[2].split("：")[1]
        job_desc = response.xpath("//div[@class='text']").xpath('string()').getall()
        job_desc = "".join(job_desc).strip()
        company = response.xpath("//*[@id='main']/div[3]/div/div[2]/div[3]/div[4]/div[1]").xpath('string()').get()
        item = BossItem(city=city,salary=salary,name=name,experience=experience,education=education,job_desc=job_desc,company=company)
        yield item