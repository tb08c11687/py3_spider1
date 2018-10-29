from selenium import webdriver
import requests
from lxml import etree
import time
import re
import requests, sys
from urllib import parse, request
import ssl
import base64


class Bossspider():
    driver_path = "./chromedriver"
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=Bossspider.driver_path)
        self.url = "https://www.zhipin.com/job_detail/?query=python&scity=100010000&industry=&position="
        self.domain = "https://www.zhipin.com/"
    def run(self):
        self.driver.get(self.url)
        while True:
            if len(self.driver.find_elements_by_id("captcha")) > 0:
                # self.driver.find_element_by_id() 返回一个element元素对象
                # self.driver.find_elements_by_id() 返回一个列表
                self.fill_captcha()
                time.sleep(2)
                continue
            source = self.driver.page_source
            self.parse_list_page(source)
            next_btn = self.driver.find_element_by_xpath("//a[@ka='page-next']")
            if "disabled" in next_btn.get_attribute('class'):
                break
            else:
                next_btn.click()

    def get_captcha(self,filepath):
        src = self.driver.find_element_by_class_name('code')
        src = src.get_attribute('src')
        request.urlretrieve(scr, "captcha.png")
        with open(filepath, 'rb') as fp:
            return fp.read()

    def fill_captcha(self):
        captchaInput = self.driver.find_element_by_id("captcha")
        submitBtn = self.driver.find_element_by_class_name("btn")
        host = 'https://302307.market.alicloudapi.com'
        path = '/ocr/captcha'
        method = 'POST'
        appcode = '3df72aac5b9147fcad60c6fdc3287c0b'
        querys = ''
        bodys = {}
        url = host + path
        headers = {'Authorization': 'APPCODE ' + appcode,
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'

                   }
        bodys['image'] = base64.b64encode(self.get_captcha('captcha'))
        bodys['type'] = '''1001'''
        post_data = parse.urlencode(bodys)
        response = requests.post(url, data=post_data, headers=headers).text
        #返回json格式
        #{"code":0,"data":{"captcha":"bmnr","id":"648161c6-1c87-47ab-9994-bcd6142b87ae"}}
        captcha = response["data"]["captcha"].strip()
        captchaInput.send_keys(captcha)
        submitBtn.click()


    def parse_list_page(self,source):
        html = etree.HTML(source)
        links = html.xpath("//div[@class='info-primary']//a/@href")
        job_url = map(lambda url:self.domain+url,links)
        for link in job_url:
            self.request_detail_page(link)
            time.sleep(1)

    def request_detail_page(self,url):
        self.driver.execute_script("window.open('%s')"%url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        source = self.driver.page_source
        self.parse_job_detail(source)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def parse_job_detail(self,source):
        positions = []
        html = etree.HTML(source)
        info_primary = html.xpath("//div[@class='info-primary']/p/text()")
        city = re.sub(r"[城市：]","",info_primary[0])
        experience = re.sub(r"[经验：]","",info_primary[1])
        education = re.sub(r"[学历：]","",info_primary[2])
        salary = html.xpath("//span[@class='badge']/text()")[0].strip()
        try:
            company = html.xpath("//div[@class='job-sec']/div[@class='name']/text()")[0]
        except Exception as e:
            print(e)
            company = "无工商信息，估计是传销"
        desc = html.xpath("//div[@class='job-sec']/div[@class='text'][position()=1]/text()")
        job_desc = "\n".join(desc).strip()
        position = [city,experience,education,salary,company,job_desc]



        positions.append(position)
        print(position)
    def store_position(self):
        pass
if __name__ == '__main__':
    spider = Bossspider()
    spider.run()