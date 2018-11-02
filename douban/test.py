#
import requests
from urllib.request import urlretrieve
from base64 import b64encode
from urllib import parse
import time
def regonize_captcha():
    #urlretrieve(image_url, 'captcha.png')
    regonize_url = 'http://imgurlocr.market.alicloudapi.com/urlimages'
    formdata = {}
    with open('captcha.png', 'rb') as fp:
        data = fp.read()
        #
        formdata['image'] = "data:image/png;base64," + b64encode(data).decode()
    AppCode = '3df72aac5b9147fcad60c6fdc3287c0b'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Authorization': 'APPCODE ' + AppCode
    }
    response = requests.post(regonize_url, data=formdata, headers=headers)
    print(response.text)
    # result = response.json()
    # print(result)
    # code = result['result'][0]['words']
    # return code
regonize_captcha()
