# -*- coding: utf-8 -*-
import scrapy

from ..items import QsbkItem
class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base_doamin = "https://www.qiushibaike.com"
    def parse(self, response):
        article_info = response.xpath("//div[@id='content-left']/div")
        for article in article_info:
            author = article_info.xpath(".//h2/text()").get()
            content = article_info.xpath(".//div[@class='content']//text()").getall()
            content = "".join(content).strip()
            item = QsbkItem(author=author,content=content)
            yield item
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            url = self.base_doamin + next_url
            print("="*50)
            print(url)
            yield scrapy.Request(url,callback=self.parse)
