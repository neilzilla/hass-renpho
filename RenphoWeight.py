import requests
import json
import datetime
from concurrent.futures import ThreadPoolExecutor
import asyncio
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64encode
import logging

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
        self.user_id = user_id
        self.weight = None
        self.time_stamp = None
        self.session_key = None  # Initialize session_key
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def _request(self, method, url, **kwargs):
        """
        Asynchronous method to make an API request and handle errors.
        """
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            self.executor, requests.request, method, url, **kwargs
        )
        response.raise_for_status()
        return response.json()

    async def auth(self):
        """
        Authenticate with the Renpho API to obtain a session key.
        """
        if not self.email or not self.password:
            raise Exception("Email and password must be provided")

        key = RSA.importKey(self.public_key)
        cipher = PKCS1_v1_5.new(key)
        encrypted_password = b64encode(cipher.encrypt(self.password.encode("utf-8")))

        data = {'secure_flag': 1, 'email': self.email, 'password': encrypted_password}
        parsed = await self._request('POST', API_AUTH_URL, data=data)

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

    async def getScaleUsers(self):
        """
        Fetch the list of users associated with the scale.
        """
        url = f"{API_SCALE_USERS_URL}?locale=en&terminal_user_session_key={self.session_key}"
        parsed = await self._request('GET', url)
        self.set_user_id(parsed['scale_users'][0]['user_id'])
        return parsed['scale_users']

    async def getMeasurements(self):
        """
        Fetch the most recent weight measurements for the user.
        """
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        week_ago_timestamp = int(time.mktime(week_ago.timetuple()))
        url = f"{API_MEASUREMENTS_URL}?user_id={self.user_id}&last_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        parsed = await self._request('GET', url)
        last_measurement = parsed['last_ary'][0]
        self.weight = last_measurement['weight']
        self.time_stamp = last_measurement['time_stamp']
        return parsed['last_ary']

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

    def getSpecificMetricFromUserID(self, metric, user_id=None):
        """
        Fetch a specific metric for a particular user ID from the most recent weight measurement.

        Args:
            metric (str): The metric to fetch (e.g., 'bodyfat', 'water', 'bmr').
            user_id (str, optional): The user ID for whom the metric should be fetched.
                                    Defaults to the object's user_id if not provided.

        Returns:
            float: Value of the specified metric, None if an error occurs or metric not found.
        """
        if user_id:
            self.set_user_id(user_id)  # Update the user_id if provided

        last_measurement = self.getMeasurements()[0]
        return last_measurement.get(metric, None)  # Return None if metric not found

    def getInfo(self):
        """
        Wrapper method to authenticate, fetch users, and get measurements.
        """
        self.auth()
        self.getScaleUsers()
        self.getMeasurements()

    def startPolling(self, polling_interval=60):
        """
        Start polling for weight data at a given interval.
        """
        self.getInfo()
        self.polling = Interval(polling_interval, self.getInfo)
        self.polling.start()

    def stopPolling(self):
        """
        Stop polling for weight data.
        """
        if hasattr(self, 'polling'):
            self.polling.cancel()


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