import requests

import json
import time
import datetime
from homeassistant.const import MASS_KILOGRAMS, MASS_POUNDS
from .types import Measurements
#from aiohttp import ClientSession
import logging

_LOGGER = logging.getLogger(__name__)

class RenphoWeight():
    def __init__ (self, email, password_hash, session, unit_of_measurements = MASS_KILOGRAMS):
        self.email = email
        self.password = password_hash
        self.session = session
        
        self.session_key = None
        self.user_id = None
        self.account_name = None

        if unit_of_measurements != MASS_KILOGRAMS : 
            self.unit_of_measurements = MASS_POUNDS
        else:
            self.unit_of_measurements = MASS_KILOGRAMS

    async def _async_auth(self):
        #_LOGGER = logging.getLogger(__name__)

        data = {
            'secure_flag': 1,
            'email': self.email,
            'password': self.password
        }

        url = 'https://renpho.qnclouds.com/api/v3/users/sign_in.json?app_id=Renpho'
        resp = await self.session.post(url, data=data)
        data = await resp.json(content_type=None)
        
        self.session_key = data['terminal_user_session_key']
        self.user_id = data['id']
        self.account_name = data['account_name']
        _LOGGER.debug('RENPHO - session_key = ' + str(self.session_key))
        _LOGGER.debug('RENPHO - account_name = ' + str(self.account_name))
        _LOGGER.debug('RENPHO - user_id = ' + str(self.user_id))


    async def _async_getMeasurements(self):
        #Todo retourner une entité Measurements à la place du json direct.
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        week_ago = int(time.mktime(week_ago.timetuple()))

        url = 'https://renpho.qnclouds.com/api/v2/measurements/list.json?user_id=' + str(self.user_id) + '&last_at=' + str(week_ago) + '&locale=en&app_id=Renpho&terminal_user_session_key=' + str(self.session_key)
        resp = await self.session.get(url)
        data = await resp.json(content_type=None)
        _LOGGER.debug('RENPHO - Got Measurements successfully')
        
        parsed_data = data['last_ary'][0]
        
        #Return the first of the last measurements on the renpho API.  Should be the latest for the main user.
        return Measurements(weight = parsed_data['weight'], 
                            created_at = parsed_data['created_at'],
                            bodyfat = parsed_data['bodyfat'],
                            water = parsed_data['water'],
                            bmr = parsed_data['bmr'],
                            bodyage = parsed_data['bodyage'],
                            bone = parsed_data['bone'],
                            subfat = parsed_data['subfat'],
                            visfat = parsed_data['visfat'],
                            bmi = parsed_data['bmi'],
                            sinew = parsed_data['sinew'],
                            protein = parsed_data['protein'],
                            fat_free_weight = parsed_data['fat_free_weight'],
                            muscle = parsed_data['muscle'],
                            user_id = self.user_id,
                            account_name = self.account_name,
                            unit_of_measurements = self.unit_of_measurements
                            )

    async def async_getInfo(self):
        await self._async_auth()
        return await self._async_getMeasurements()
        