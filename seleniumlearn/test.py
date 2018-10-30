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



def get_captcha(filepath):
    driver_path = "./chromedriver"
    driver = webdriver.Chrome(executable_path=driver_path)
    url = "https://www.zhipin.com/captcha/popUpCaptcha?redirect=https%3A%2F%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3Dpython%26scity%3D100010000%26industry%3D%26position%3D"
    driver.get(url)
    source = driver.page_source
    src = driver.find_element_by_class_name('code')
    link = src.get_attribute('src')
    request.urlretrieve(link, "captcha.png")
    with open(filepath, 'rb') as fp:
        return fp.read()
def fill_captcha():
    driver_path = "./chromedriver"
    driver = webdriver.Chrome(executable_path=driver_path)
    url = "https://www.zhipin.com/captcha/popUpCaptcha?redirect=https%3A%2F%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3Dpython%26scity%3D100010000%26industry%3D%26position%3D"
    driver.get(url)
    captchaInput = driver.find_element_by_id("captcha")
    submitBtn = driver.find_element_by_class_name("btn")
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
    bodys['image'] = base64.b64encode(get_captcha("captcha.png"))
    bodys['type'] = '''1001'''
    post_data = parse.urlencode(bodys)
    response = eval(requests.post(url, data=post_data, headers=headers).text)
    print(response)
    # 返回字符串式！！！！！！！！！！！！
    # {"code":0,"data":{"captcha":"bmnr","id":"648161c6-1c87-47ab-9994-bcd6142b87ae"}}
    captcha = response["data"]["captcha"].strip()
    print(captcha)
    captchaInput.send_keys(captcha)
    submitBtn.click()

if __name__ == '__main__':
    fill_captcha()