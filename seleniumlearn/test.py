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



# def get_captcha(filepath):
#     driver_path = "./chromedriver"
#     driver = webdriver.Chrome(executable_path=driver_path)
#     url = "https://www.baidu.com"
#     driver.get(url)
#     source = driver.page_source
#     src = driver.find_element_by_class_name('code')
#     link = src.get_attribute('src')
#     request.urlretrieve(link, "captcha.png")
#     with open(filepath, 'rb') as fp:
#         return fp.read()
def fill_captcha():
    url = "https://www.baidu.com"
    driver_path = "./chromedriver"
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(url)
    driver.execute_script("window.open('%s')" % "http://www.duowan.com")
    print(driver.current_window_handle)
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])


    print(driver.current_window_handle)
    time.sleep(5)
    driver.close()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[0])



if __name__ == '__main__':
    fill_captcha()