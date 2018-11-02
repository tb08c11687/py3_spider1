from selenium import webdriver
import requests
from lxml import etree
import time
import re
import requests, sys
from urllib import parse, request
import ssl
import base64
from openpyxl import Workbook
import simplejson
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Bossspider():
    driver_path = "./chromedriver"
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=Bossspider.driver_path)
        self.url = "https://www.zhipin.com/job_detail/?query=python&scity=100010000&industry=&position="
        self.domain = "https://www.zhipin.com/"
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(["城市", "工作经验", "学历", "薪资", "公司", "职位要求"])
    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            self.parse_list_page(source)
            next_btn = self.driver.find_element_by_xpath("//a[@ka='page-next']")
            if "disabled" in next_btn.get_attribute('class'):
                break
            else:
                next_btn.click()

    def get_captcha(self,filepath):
        src = self.driver.find_element_by_class_name('code')
        link = src.get_attribute('src')
        request.urlretrieve(link, "captcha.png")
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
        bodys['image'] = base64.b64encode(self.get_captcha("captcha.png"))
        bodys['type'] = '''1001'''
        post_data = parse.urlencode(bodys)
        response = eval(requests.post(url, data=post_data, headers=headers).text)
        print(response)
        #返回字符串式！！！！！！！！！！！！
        #{"code":0,"data":{"captcha":"bmnr","id":"648161c6-1c87-47ab-9994-bcd6142b87ae"}}
        captcha = response["data"]["captcha"].strip()
        print(captcha)
        captchaInput.send_keys(captcha)
        time.sleep(3)
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
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1])
        source = self.driver.page_source
        self.parse_job_detail(source)
        time.sleep(3)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def parse_job_detail(self,source):

        html = etree.HTML(source)

        while len(self.driver.find_elements_by_id("captcha")) > 0:
            # self.driver.find_element_by_id() 返回一个element元素对象
            # self.driver.find_elements_by_id() 返回一个列表
            self.fill_captcha()
            time.sleep(2)
        else:
            # if len(html.xpath("//div[@class='info-primary']/p/text()")) >0:
            #     break
            try:
                WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"info-primary")))
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

                self.store_position(position)
            except Exception as e:
                print(e)
                self.driver.close()
            #
    def store_position(self,position):
        self.ws.append(position)
        self.wb.save("./Boss.xlsx")
if __name__ == '__main__':
    spider = Bossspider()
    spider.run()