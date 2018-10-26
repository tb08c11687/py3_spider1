import requests
from lxml import etree
import simplejson
import time
from bs4 import BeautifulSoup
HEADER ={
        "Cookie": "PHPSESSID=8ir8s188dp7k6r5sjjoe32p946; pgv_pvi=877227008; pgv_si=s8137142272",
        "Referer": "https://hr.tencent.com/social.php",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.100 Chrome/69.0.3497.100 Safari/537.36",
        "pgrade-Insecure-Requests": "1"
    }
def get_detail_url(url):
    #获取初始（种子）网页
    response = requests.get(url,headers=HEADER)
    #解析网页
    html = etree.HTML(response.text)
    page_numbers = html.xpath("//div[@class='pagenav']//a/text()")[-2]
    #获取岗位详情链接
    detail_url = html.xpath("//tr[@class='even']//a/@href")
    base_url = "https://hr.tencent.com/"
    links = map(lambda url:base_url+url,detail_url)
    return links,page_numbers

def parse_detail(url):
    position = {}
    response = requests.get(url,headers=HEADER)
    html = etree.HTML(response.text)
    soup = BeautifulSoup(html, "lxml")
    # print(soup.prettify())
    trs = soup.find_all('tr', class_="squareli")
    for tr in trs:
        position = {}
        infos = list(tr.stripped_strings)
        position['title'] = infos[0]
        position['categray'] = infos[1]
        position['location'] = infos[3]
        position['time'] = infos[4]
        print(position)
    duty = work_info[0].xpath(".//text()")
    require = work_info[1].xpath(".//text()")
    position['duty'] = duty
    position['require'] = require
    return position
def spider():
    positions = []
    urls, page_number = get_detail_url("https://hr.tencent.com/position.php?lid=&tid=&keywords=python&start=0#a")
    for i in range(0,int(page_number)):
        time.sleep(5)
        KEYWORD = "python"
        START_URL = "https://hr.tencent.com/position.php?lid=&tid=&keywords={}&start={}#a".format(KEYWORD,i*10)
        urls, page_number = get_detail_url(START_URL)
        for url in urls:
            time.sleep(3)
            position = parse_detail(url)
            print("+++++++++++"*50,position)
            positions.append(position)
        with open('tencent.json','w',encoding='utf-8') as f:
            simplejson.dump(positions,f)

    return positions




if __name__ == '__main__':
    spider()
