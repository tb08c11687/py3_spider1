
import requests
from urllib.request import urlretrieve
from base64 import b64decode
def regonize_captcha(image_url):
    #urlretrieve(image_url, 'captcha.png')
    regonize_url = 'http://imgurlocr.market.alicloudapi.com/urlimages'
    formdata = {}
    with open('captcha.png', 'rb') as fp:
        data = fp.read()
        pic = b64decode(data)
        formdata['image'] = pic
    AppCode = '3df72aac5b9147fcad60c6fdc3287c0b'
    headers = {

        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Authorization': 'APPCODE ' + AppCode
    }

    response = requests.post(regonize_url, data=formdata, headers=headers)
    print(response.content)
    #result = response.json()
    # print(result)
    # code = result['result']['code']
    # return code
regonize_captcha('https://www.douban.com/misc/captcha?id=a2rUMyxShlxrVqfjoEJW9jKH:en&size=s')