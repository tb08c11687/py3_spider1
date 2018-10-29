from selenium import webdriver
import requests
from lxml import etree
import time
import re
import requests, sys
from urllib import parse, request
import ssl
import base64
import xlsxwriter
driver_path = "./chromedriver"



driver = webdriver.Chrome(executable_path=driver_path)
url = "https://www.zhipin.com/captcha/popUpCaptcha?redirect=https%3A%2F%2Fwww.zhipin.com%2F%2Fjob_detail%2F9b31e3751c6829650n152N-8FA~~.html"
domain = "https://www.zhipin.com/"
driver.get(url)
source = driver.page_source
src = driver.find_elements_by_class_name('code')
print(type(src))
print(src)
src = driver.find_element_by_class_name('code')
print(type(src))
print(src)
# src = src.get_attribute('src')
#
# print(src)
# request.urlretrieve(src,"captcha.png")
# def get_image(url):
#     with open(url, 'rb') as fp:
#         return fp.read()
# get_image('./captcha.png')

# url = "url=https%3A%2F%2Fwww.zhipin.com%2F%2Fjob_detail%2F9b31e3751c6829650n152N-8FA~~.html"
# print(url.encode("utf-8").decode())
# print(parse.parse_qs(url))
# jsonstr = {"code":0,"data":{"captcha":"bmnr","id":"648161c6-1c87-47ab-9994-bcd6142b87ae"}}
# print(type(jsonstr["data"]["captcha"]))