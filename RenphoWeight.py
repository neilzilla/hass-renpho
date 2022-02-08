import requests
import json
import time
import datetime
from homeassistant.const import MASS_KILOGRAMS, MASS_POUNDS
from threading import Timer

import logging
_LOGGER = logging.getLogger(__name__)


class Interval(Timer):
  def run(self):
    while not self.finished.wait(self.interval):
      self.function(*self.args, **self.kwargs)

class RenphoWeight():
    def __init__ (self, email, password_hash, unit_of_measurements):
        self.email = email
        self.password = password_hash
        
        self.unit_of_measurements = MASS_KILOGRAMS
        if unit_of_measurements != MASS_KILOGRAMS:
            self.unit_of_measurements = MASS_POUNDS




        self.weight = None
        self.created_at = None
        self.bodyfat = None
        self.water = None
        self.bmr = None
        self.bodyage = None
        self.bone = None
        self.subfat = None
        self.visfat = None
        self.bmi = None
        self.sinew = None
        self.protein = None
        self.fat_free_weight = None
        self.muscle = None

    def auth(self):
        data = {
            'secure_flag': 1,
            'email': self.email,
            'password': self.password
        }

        r = requests.post(url = 'https://renpho.qnclouds.com/api/v3/users/sign_in.json?app_id=Renpho', data = data)
        
        parsed = json.loads(r.text)
        self.session_key = parsed['terminal_user_session_key']
        self.user_id = parsed['id']

    def getMeasurements(self):

        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        week_ago = int(time.mktime(week_ago.timetuple()))

        r = requests.get('https://renpho.qnclouds.com/api/v2/measurements/list.json?user_id=' + str(self.user_id) + '&last_at=' + str(week_ago) + '&locale=en&app_id=Renpho&terminal_user_session_key=' + str(self.session_key))
        
        measurements = json.loads(r.text)
        
        last = measurements['last_ary'][0]

        self.weight = last['weight']
        self.created_at = last['created_at']

        self.bodyfat = last['bodyfat']
        self.water = last['water']
        self.bmr = last['bmr']
        self.bodyage = last['bodyage']
        self.bone = last['bone']
        self.subfat = last['subfat']
        self.visfat = last['visfat']
        self.bmi = last['bmi']
        self.sinew = last['sinew']
        self.protein = last['protein']
        self.fat_free_weight = last['fat_free_weight']
        self.muscle = last['muscle']

        return json.loads(r.text)['last_ary']

    def getInfo(self):
        try:
          self.auth()
          self.getMeasurements()
        except:
          _LOGGER = logging.error('error in polling')
    
    def startPolling(self, polling_interval=60):
        self.getInfo()
        self.polling = Interval(polling_interval, self.getInfo) 
        self.polling.start()

    def stopPolling(self):
        if self.polling:
            self.polling.cancel()
