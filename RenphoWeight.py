from threading import Timer
import requests
import json
import datetime
import asyncio
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64encode
import logging
import time
import aiohttp
from typing import Optional, List, Dict

# Initialize logging
_LOGGER = logging.getLogger(__name__)

# API Endpoints
API_AUTH_URL = 'https://renpho.qnclouds.com/api/v3/users/sign_in.json?app_id=Renpho'
API_SCALE_USERS_URL = 'https://renpho.qnclouds.com/api/v3/scale_users/list_scale_user'
API_MEASUREMENTS_URL = 'https://renpho.qnclouds.com/api/v2/measurements/list.json'

class RenphoWeight:
    """
    A class to interact with Renpho's weight scale API.

    Attributes:
        public_key (str): The public RSA key used for encrypting the password.
        email (str): The email address for the Renpho account.
        password (str): The password for the Renpho account.
        user_id (str, optional): The ID of the user for whom weight data should be fetched.
        weight (float): The most recent weight measurement.
        time_stamp (int): The timestamp of the most recent weight measurement.
        session_key (str): The session key obtained after successful authentication.
        executor (ThreadPoolExecutor): Executor for running synchronous requests.
    """

    def __init__(self, public_key, email, password, user_id=None):
        """Initialize a new RenphoWeight instance."""
        self.public_key = public_key
        self.email = email
        self.password = password
        if user_id == ""
            self.user_id = None
        self.user_id = user_id
        self.weight = None
        self.time_stamp = None
        self.session_key = None

    async def _request(self, method, url, **kwargs):
        """
        Asynchronous method to make an API request and handle errors.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, **kwargs) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            _LOGGER.error(f"Error in request: {e}")
            raise  # Or raise a custom exception

    def _requestSync(self, method, url, **kwargs):
        """
        Make a generic API request and handle errors.
        """
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            _LOGGER.error(f"Error in request: {e}")
            raise  # Or raise a custom exception

    def authSync(self):
        """
        Authenticate with the Renpho API to obtain a session key.
        """
        if not self.email or not self.password:
            raise Exception("Email and password must be provided")

        key = RSA.importKey(self.public_key)
        cipher = PKCS1_v1_5.new(key)
        encrypted_password = b64encode(cipher.encrypt(self.password.encode("utf-8")))

        data = {'secure_flag': 1, 'email': self.email, 'password': encrypted_password}
        parsed = self._requestSync('POST', API_AUTH_URL, data=data)

        if 'terminal_user_session_key' not in parsed:
            raise Exception("Authentication failed.")

        self.session_key = parsed['terminal_user_session_key']
        return parsed

    async def auth(self):
        """
        Authenticate with the Renpho API to obtain a session key.
        """
        if not self.email or not self.password:
            raise Exception("Email and password must be provided")

        key = RSA.importKey(self.public_key)
        cipher = PKCS1_v1_5.new(key)
        encrypted_password = b64encode(cipher.encrypt(self.password.encode("utf-8")))

        data = {'secure_flag': '1', 'email': self.email, 'password': encrypted_password}
        parsed = await self._request('POST', API_AUTH_URL, json=data)

        if 'terminal_user_session_key' not in parsed:
            raise Exception("Authentication failed.")

        self.session_key = parsed['terminal_user_session_key']
        return parsed

    async def validate_credentials(self):
        """
        Validate the current credentials by attempting to authenticate.
        Returns True if authentication succeeds, False otherwise.
        """
        try:
            await self.auth()
            return True
        except Exception as e:
            _LOGGER.error(f"Validation failed: {e}")
            return False

    def getScaleUsersSync(self):
        """
        Fetch the list of users associated with the scale.
        """
        url = f"{API_SCALE_USERS_URL}?locale=en&terminal_user_session_key={self.session_key}"
        parsed = self._requestSync('GET', url)
        self.set_user_id(parsed['scale_users'][0]['user_id'])
        return parsed['scale_users']

    async def getScaleUsers(self):
        """
        Fetch the list of users associated with the scale.
        """
        url = f"{API_SCALE_USERS_URL}?locale=en&terminal_user_session_key={self.session_key}"
        parsed = await self._request('GET', url)
        self.set_user_id(parsed['scale_users'][0]['user_id'])
        return parsed['scale_users']

    def getMeasurementsSync(self) -> Optional[List[Dict]]:
        """
        Fetch the most recent weight measurements for the user.
        """
        try:
            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=7)
            week_ago_timestamp = int(time.mktime(week_ago.timetuple()))
            url = f"{API_MEASUREMENTS_URL}?user_id={self.user_id}&last_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
            parsed = self._requestSync('GET', url)
            
            if 'last_ary' not in parsed:
                _LOGGER.warning(f"Field 'last_ary' is not in the response: {parsed}")
                return None

            last_measurement = parsed['last_ary'][0]
            self.weight = last_measurement.get('weight', None)
            self.time_stamp = last_measurement.get('time_stamp', None)
            return parsed['last_ary']
        except Exception as e:
            _LOGGER.error(f"An error occurred: {e}")
            return None


    async def getMeasurements(self) -> Optional[List[Dict]]:
        """
        Fetch the most recent weight measurements for the user.
        """
        try:
            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=7)
            week_ago_timestamp = int(time.mktime(week_ago.timetuple()))
            url = f"{API_MEASUREMENTS_URL}?user_id={self.user_id}&last_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
            parsed = await self._request('GET', url)
            
            if 'last_ary' not in parsed:
                _LOGGER.warning(f"Field 'last_ary' is not in the response: {parsed}")
                return None

            last_measurement = parsed['last_ary'][0]
            self.weight = last_measurement.get('weight', None)
            self.time_stamp = last_measurement.get('time_stamp', None)
            return parsed['last_ary']
        except Exception as e:
            _LOGGER.error(f"An error occurred: {e}")
            return None

    def getSpecificMetricSync(self, metric: str) -> Optional[float]:
        """
        Synchronous version of getSpecificMetric.
        """
        try:
            last_measurement = self.getMeasurementsSync()  # Assuming you have a synchronous version of getMeasurements
            if last_measurement:
                return last_measurement[0].get(metric, None)
            return None
        except Exception as e:
            _LOGGER.error(f"An error occurred: {e}")
            return None

    async def getSpecificMetric(self, metric: str) -> Optional[float]:
        """
        Fetch a specific metric from the most recent weight measurement.
        """
        try:
            last_measurement = await self.getMeasurements()
            if last_measurement:
                return last_measurement[0].get(metric, None)
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    async def getSpecificMetricFromUserID(self, metric: str, user_id: Optional[str] = None) -> Optional[float]:
        """
        Fetch a specific metric for a particular user ID from the most recent weight measurement.
        """
        try:
            if user_id:
                self.set_user_id(user_id)  # Update the user_id if provided
            
            last_measurement = await self.getMeasurements()
            if last_measurement:
                return last_measurement[0].get(metric, None)
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def getInfoSync(self):
        """
        Wrapper method to authenticate, fetch users, and get measurements.
        """
        self.authSync()
        self.getScaleUsersSync()
        self.getMeasurementsSync()

    async def getInfo(self):
        """
        Wrapper method to authenticate, fetch users, and get measurements.
        """
        await self.auth()
        await self.getScaleUsers()
        await self.getMeasurements()

    async def startPolling(self, polling_interval=60):
        """
        Start polling for weight data at a given interval.
        """
        await self.getInfo()
        while True:
            await asyncio.sleep(polling_interval)
            await self.getInfo()

    def stopPolling(self):
        """
        Stop polling for weight data.
        """
        if hasattr(self, 'polling'):
            self.polling.cancel()

    def set_user_id(self, user_id):
        """
        Set the user ID for whom the weight data should be fetched.
        """
        self.user_id = user_id

    def get_user_id(self):
        """
        Get the current user ID for whom the weight data is being fetched.
        """
        return self.user_id

    def close(self):
        """
        Shutdown the executor when you are done using the RenphoWeight instance.
        """
        self.executor.shutdown()

class Interval(Timer):
    """
    A subclass of Timer to repeatedly run a function at a specified interval.
    """

    def run(self):
        """
        Run the function at the given interval.
        """
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)