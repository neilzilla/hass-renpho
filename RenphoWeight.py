import requests
import json
import time
import datetime
from threading import Timer

import logging
_LOGGER = logging.getLogger(__name__)


class Interval(Timer):
  def run(self):
    while not self.finished.wait(self.interval):
      self.function(*self.args, **self.kwargs)

class RenphoWeight():
    def __init__ (self, email, password_hash):
        self.email = email
        self.password = password_hash
        self.weight = None
        self.time_stamp = None

    def auth(self):
        data = {
            'secure_flag': 1,
            'email': self.email,
            'password': self.password
        }

        r = requests.post(url = 'https://renpho.qnclouds.com/api/v3/users/sign_in.json?app_id=Renpho', data = data)
        
        parsed = json.loads(r.text)
        self.session_key = parsed['terminal_user_session_key']
        return parsed

    def getScaleUsers(self):
        r = requests.get(url = 'https://renpho.qnclouds.com/api/v3/scale_users/list_scale_user?locale=en&terminal_user_session_key=' + self.session_key)
        parsed = json.loads(r.text)

        self.user_id = parsed['scale_users'][0]['user_id']
        return parsed['scale_users']

    def getMeasurements(self):

        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        week_ago = int(time.mktime(week_ago.timetuple()))

        r = requests.get('https://renpho.qnclouds.com/api/v2/measurements/list.json?user_id=' + self.user_id + '&last_at=' + str(week_ago) + '&locale=en&app_id=Renpho&terminal_user_session_key=' + self.session_key)
        
        measurements = json.loads(r.text)
        
        last = measurements['last_ary'][0]

        self.weight = last['weight']
        self.time_stamp = last['time_stamp']

        return json.loads(r.text)['last_ary']

    def getInfo(self):
        try:
          self.auth()
          self.getScaleUsers()
          self.getMeasurements()
        except:
          _LOGGER = logging.info('error in polling')
    
    def startPolling(self, polling_interval=60):
        self.getInfo()
        self.polling = Interval(polling_interval, self.getInfo) 
        self.polling.start()

    def stopPolling(self):
        if self.polling:
            self.polling.cancel()
