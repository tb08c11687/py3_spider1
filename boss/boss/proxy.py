
from datetime import datetime,timedelta

class ProxyModel(object):
    def __init__(self,data):
        self.ip = data['ip']
        self.port = data['port']
        self.expire_str = data['expire_time']
        self.proxy = "https://{}:{}".format(self.ip,self.port)
        self.date_time = datetime.strptime(self.expire_str, '%Y-%m-%d %H:%M:%S')
        self._expire_time = None
        self.blacked = False
    @property
    def is_expireing(self):
        now = datetime.now()
        if (self.date_time - now) < timedelta(seconds=5):
            return True
        else:
            return False

