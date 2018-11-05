import requests
import json
from datetime import datetime
response = requests.get("http://webapi.http.zhimacangku.com/getip?num=3&type=2&pro=&city=0&yys=0&port=11&time=2&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=")
result = json.loads(response.text)
#print(result)
print(result['data'][1]['expire_time'])
time = datetime.strptime(result['data'][1]['expire_time'],'%Y-%m-%d %H:%M:%S')
print(type(time))