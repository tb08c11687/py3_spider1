import requests
from  lxml import etree
from urllib import request
import os
import re
from queue import Queue
import threading
import datetime
class Producer(threading.Thread):
    header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"}
    domain = "http://www.budejie.com"
    def __init__(self,page_queue:Queue,img_queue:Queue,*args,**kwargs):
        super(Producer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            print(url)
            self.parse_page(url)
    def parse_page(self,url):
        #获取图片链接列表
        img_list_response = requests.get(url, headers=self.header).text
        html = etree.HTML(img_list_response)
        links = html.xpath("//div[@class='j-r-list-c-img']//a/@href")
        img_detail_urls = map(lambda url: self.domain + url, links)
        #获取图片链接
        for img_url in img_detail_urls:
            img_response = requests.get(img_url, headers=self.header).text
            html = etree.HTML(img_response)
            img_url = html.xpath("//div[@class='j-r-list-c-img']//img/@src")[0]
            img_title = html.xpath("//div[@class='j-r-list-c-img']//img/@title")[0]
            try:
                img_title = re.findall("\w{,48}", re.sub(r'[?？.。，！1~【】/【】～`！!@#$%^*&“”""]', '', img_title))[0]
                suffix = os.path.splitext(img_url)[1]
                file_name = img_title.strip() + suffix
                self.img_queue.put((img_url, file_name))
            except Exception as e:
                print("========================{}==================================".format(e))
            finally:
                pass
#
class Consumer(threading.Thread):
    # header = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0"}

    def __init__(self, page_queue: Queue, img_queue: Queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
    def run(self):
        while True:
            while self.img_queue.empty() and self.page_queue.empty():
                break
            img_url,file_name = self.img_queue.get()
            request.urlretrieve(img_url, '/home/yuyang/PycharmProjects/py3_spider/image/' + file_name)
            print("下载图片:{}".format(file_name))


def main():
    page_queue = Queue(500)
    img_queue = Queue(1000)
    global delta_time
    for x in range(5,50):
        base_url = "http://www.budejie.com/pic/{}".format(x)
        page_queue.put(base_url)
    for x in range(5):
        t = Producer(page_queue,img_queue).start()
    for x in range(5):
        t = Consumer(page_queue,img_queue).start()

if __name__ == '__main__':
    main()
