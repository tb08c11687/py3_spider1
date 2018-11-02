# -*- coding: utf-8 -*-
import scrapy
import requests
from urllib.request import urlretrieve
from PIL import Image
from base64 import b64encode
from urllib import parse

class DoubanLogSpider(scrapy.Spider):
    name = 'douban_log'
    allowed_domains = ['douban.com']
    start_urls = ['https://accounts.douban.com/login']
    login_url = "https://accounts.douban.com/login?source=movie"



    def parse(self, response):
        formdata = {
            'source': 'None',
            'redir': 'https://www.douban.com/',
            'form_email': '15196665336',
            'form_password': 'tb08c11687',
            'login': '登录'
        }
        captcha_url = response.xpath("//img[@id='captcha_image']/@src").get()
        if captcha_url:
            captcha = self.regonize_captcha(captcha_url)
            formdata['captcha-solution'] = captcha
            captcha_id = response.xpath("//input[@name='captcha-id']/@value").get()
            formdata['captcha-id'] = captcha_id
        yield scrapy.FormRequest(url=self.login_url,formdata=formdata,callback=self.parse_after_login)


    def parse_after_login(self,response):
        if response.url == 'https://www.douban.com/':
            print('登录成功')
        else:
            print('登录失败')


    def regonize_captcha(self,image_url):
        urlretrieve(image_url,'captcha.png')
        regonize_url = 'http://imgurlocr.market.alicloudapi.com/urlimages'
        formdata = {}
        with open('captcha.png', 'rb') as fp:
            data = fp.read()
            formdata['image'] = "data:image/jpeg;base64,"+b64encode(data).decode()

        data = parse.urlencode(formdata).encode()
        AppCode = '3df72aac5b9147fcad60c6fdc3287c0b'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'APPCODE ' + AppCode
        }
        response = requests.post(regonize_url, data=data, headers=headers)
        result = response.json()

        code = result['result'][0]['words']
        return code