import requests
from lxml import etree
from urllib import request
import re
import os
import datetime
def parse_page(url):
    domain = "http://www.budejie.com"
    header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"
              }
    response = requests.get(url,headers=header).text
    html = etree.HTML(response)
    links = html.xpath("//div[@class='j-r-list-c-img']//a/@href")
    img_detail_urls = map(lambda url:domain+url,links)
    #print(img_detail_urls)
    return img_detail_urls

def get_img(url):
    header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"
              }
    response = requests.get(url,headers=header).text
    html = etree.HTML(response)
    img_url = html.xpath("//div[@class='j-r-list-c-img']//img/@src")[0]
    #print(img_url)
    img_title = html.xpath("//div[@class='j-r-list-c-img']//img/@title")[0]
    try:
        img_title = re.findall("\w{1,20}",re.sub(r'[\?？\.，！1~【】\/【】～`！!@#$%^*&“”""]','',img_title))[0]
    except Exception as e:
        print(e)


    suffix = os.path.splitext(img_url)[1]
    #print(img_title)
    file_name = img_title.strip()+suffix
    request.urlretrieve(img_url,'/home/yuyang/PycharmProjects/py3_spider/image/'+file_name)
    print("下载图片:{}".format(file_name))



delta_time = 0
def main():
    global delta_time
    for x in range(6,50):
        start = datetime.datetime.now()
        base_url = "http://www.budejie.com/pic/{}".format(x)
        print("================开始下载第{}页====================".format(x))
        img_urls = parse_page(base_url)
        for img_url in img_urls:
            print(img_url)
            get_img(img_url)


        delta = (datetime.datetime.now() - start).seconds
        delta_time += delta
        print("================第{}页消耗时间{}秒==================".format(x, delta))
        break
    print("================下载完毕，共计耗时{}秒===============".format(delta_time))






if __name__ == '__main__':
    main()