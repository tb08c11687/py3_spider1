# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import NowHouseItem
from  ..items import EsfItem
class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['fang.com']
    start_urls = ['http://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        base_domain = "fang.com/house/s/"
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None
        for tr in trs:
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r"\s","",province_text)
            if province_text:
                province = province_text
            if province == "其它":
                continue

            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                scheme = city_url.split(".")
                if "bj." in city_url:
                    esf = "http://esf.fang.com/"
                    nowhouse = "http://newhouse.fang.com/house/s/"
                else:
                    esf = scheme[0] + ".esf." + base_domain
                    nowhouse = scheme[0] + ".newhouse." + base_domain
                #yield scrapy.Request(url=nowhouse,callback=self.parse_nowhouse,meta={"info":(province,city)})
                yield scrapy.Request(url=esf,callback=self.parse_esf,meta={"info":(province,city)})


    def parse_nowhouse(self,response):
        province,city = response.meta.get('info')
        lis = response.xpath("//div[@class='nl_con clearfix']/ul/li")
        for li in lis:

            if li.xpath(".//div[@class = 'clearfix']/h3"):
                continue
            name = li.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()
            rooms = li.xpath(".//div[@class='house_type clearfix']/a/text()").getall()
            rooms = list(map(lambda x:re.sub(r'\s',"",x),rooms))
            rooms = list(filter(lambda x:x.endswith("居"),rooms))
            area = "".join(li.xpath(".//div[@class='house_type clearfix']/text()").getall())
            area = re.sub(r'\s|－|/','',area)
            #rooms = "".join(rooms).strip()
            address = li.xpath(".//div[@class='address']/a/@title").get()
            district = "".join(li.xpath(".//div[@class='address']/a//text()").getall())
            district = re.search(r".*\[(.+)\].*",district).group(1)
            sale = li.xpath(".//div[@class='fangyuan pr']/span/text()").get()
            price = "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
            price = re.sub(r"\s|广告","",price)
            origin_url = li.xpath(".//div[@class='nlcd_name']/a/@href").get()

            item = NowHouseItem(name=name,rooms=rooms,area=area,address=address,district=district,sale=sale,price=price,origin_url=origin_url,province=province,city=city)
            yield item
        next_url = response.xpath("//div[@class='page']/a[@class='next']/@href").get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_nowhouse,meta={"info":(province,city)})

    def parse_esf(self,response):
        province, city = response.meta.get('info')
        dls = response.xpath("//div[@class='shop_list shop_list_4']/dl")
        for dl in dls:

            name = dl.xpath(".//p[@class='add_shop']/a/@title").get()
            item = EsfItem(province=province, city=city,name=name)
            infos = dl.xpath(".//p[@class='tel_shop']/text()").getall()
            infos = list(map(lambda x:re.sub(r'\s',"",x),infos))

            for info in infos:
                #print(info)
                if "厅" in info:
                    item['rooms'] = info
                elif "㎡" in info:
                    item['area'] = info
                elif "层" in info:
                    item['floor'] = info
                elif "向" in info:
                    item['toward'] = info
                elif "年建" in info:
                    item['years'] = info.replace("年建","")
            item['address'] = dl.xpath(".//p[@class='add_shop']/span").xpath("string()").get()
            item['price'] = dl.xpath(".//span[@class='red']/b/text()").get()
            unit = dl.xpath(".//dd[@class='price_right']//span[2]").xpath("string()").get()
            if unit:
                item['unit'] = unit.replace("元/㎡","")
            item['origin_url'] = response.urljoin(dl.xpath(".//h4[@class='clearfix']/a/@href").get())
            yield item
        next_url = response.xpath("//div[@class='page_al']//p[1]/a/@href").get()

        yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_esf,meta={"info":(province,city)})




