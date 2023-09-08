import requests
import json
import time
import datetime
from threading import Timer
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
    """

    def __init__(self, public_key, email, password, user_id=None):
        """
        Initialize a new RenphoWeight instance.
        """
        _LOGGER.debug("Init RenphoWeight")
        self.public_key = public_key
        self.email = email
        self.password = password
        self.user_id = user_id
        self.weight = None
        self.time_stamp = None
        self.session_key = None  # Initialize session_key

    def _request(self, method, url, **kwargs):
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

    def auth(self):
        """
        Authenticate with the Renpho API to obtain a session key.
        """

        if not self.email:
            raise Exception("Email must be provided")

        if not self.password:
            raise Exception("Password must be provided")

        # Encrypt the password using RSA encryption
        key = RSA.importKey(self.public_key)
        cipher = PKCS1_v1_5.new(key)
        encrypted_password = b64encode(
            cipher.encrypt(self.password.encode("utf-8")))

        # Make the authentication request
        data = {'secure_flag': 1, 'email': self.email,
                'password': encrypted_password}
        parsed = self._request('POST', API_AUTH_URL, data=data)

        if 'terminal_user_session_key' not in parsed:
            raise Exception("Authentication failed. Please check your username and password.")


        # Store the session key
        self.session_key = parsed['terminal_user_session_key']
        return parsed

    def validate_credentials(self):
        """
        Validate the current credentials by attempting to authenticate.

        Returns:
            bool: True if authentication succeeds, False otherwise.
        """
        try:
            self.auth()
            return True
        except Exception as e:
            _LOGGER.error(f"Validation failed: {e}")
            return False

    def getScaleUsers(self):
        """
        Fetch the list of users associated with the scale.
        """
        url = f"{API_SCALE_USERS_URL}?locale=en&terminal_user_session_key={self.session_key}"
        parsed = self._request('GET', url)
        self.set_user_id(parsed['scale_users'][0]['user_id'])
        return parsed['scale_users']

    def getMeasurements(self):
        """
        Fetch the most recent weight measurements for the user.
        """
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        week_ago_timestamp = int(time.mktime(week_ago.timetuple()))
        url = f"{API_MEASUREMENTS_URL}?user_id={self.user_id}&last_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        parsed = self._request('GET', url)
        last_measurement = parsed['last_ary'][0]
        self.weight = last_measurement['weight']
        self.time_stamp = last_measurement['time_stamp']
        return parsed['last_ary']

    def getSpecificMetric(self, metric):
        """
        Fetch a specific metric from the most recent weight measurement.
        """
        last_measurement = self.getMeasurements()[0]
        # Return None if metric not found
        return last_measurement.get(metric, None)

    def set_user_id(self, user_id):
        """
        Set the user ID for whom the weight data should be fetched.

        Args:
            user_id (str): The new user ID.
        """
        self.user_id = user_id

    def get_user_id(self):
        """
        Get the current user ID for whom the weight data is being fetched.

        Returns:
            str: The current user ID.
        """
        return self.user_id

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
