import asyncio
import datetime
import json
import logging
import time
from base64 import b64encode
from threading import Timer
from typing import Dict, List, Optional, Union

import aiohttp
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

# Initialize logging
_LOGGER = logging.getLogger(__name__)

# API Endpoints
API_AUTH_URL = "https://renpho.qnclouds.com/api/v3/users/sign_in.json?app_id=Renpho"
API_SCALE_USERS_URL = "https://renpho.qnclouds.com/api/v3/scale_users/list_scale_user"
API_MEASUREMENTS_URL = "https://renpho.qnclouds.com/api/v2/measurements/list.json"
DEVICE_INFO_URL = "https://renpho.qnclouds.com/api/v2/device_binds/get_device.json"
LATEST_MODEL_URL = "https://renpho.qnclouds.com/api/v3/devices/list_lastest_model.json"
GIRTH_URL = "https://renpho.qnclouds.com/api/v3/girths/list_girth.json"
GIRTH_GOAL_URL = "https://renpho.qnclouds.com/api/v3/girth_goals/list_girth_goal.json"
GROWTH_RECORD_URL = (
    "https://renpho.qnclouds.com/api/v3/growth_records/list_growth_record.json"
)


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

    def __init__(self, public_key, email, password, user_id=None, refresh=None):
        """Initialize a new RenphoWeight instance."""
        self.public_key = public_key
        self.email = email
        self.password = password
        if user_id == "":
            self.user_id = None
        self.user_id = user_id
        self.weight = None
        self.time_stamp = None
        self.session_key = None
        if refresh is None:
            self.refresh = 60
        self.session = aiohttp.ClientSession()

    @staticmethod
    def get_week_ago_timestamp() -> int:
        week_ago = datetime.date.today() - datetime.timedelta(days=7)
        return int(time.mktime(week_ago.timetuple()))

    def prepare_data(self, data):
        if isinstance(data, bytes):
            return data.decode("utf-8")
        elif isinstance(data, dict):
            return {key: self.prepare_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.prepare_data(element) for element in data]
        else:
            return data

    async def _request(self, method: str, url: str, **kwargs) -> Union[Dict, List]:
        try:
            kwargs = self.prepare_data(kwargs)
            # Reuse session
            async with self.session.request(method, url, **kwargs) as response:
                response.raise_for_status()
                parsed_response = await response.json()

                if parsed_response.get("status_code") == "40302":
                    await self.auth()

                return parsed_response
        except Exception as e:
            _LOGGER.error(f"Error in request: {e}")
            raise APIError("API request failed")  # Raise a custom exception

    def _request_sync(self, method: str, url: str, **kwargs) -> Union[Dict, List]:
        try:
            kwargs = self.prepare_data(kwargs)  # Update this line
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            _LOGGER.error(f"Error in request: {e}")
            raise  # Or raise a custom exception

    def auth_sync(self):
        """
        Authenticate with the Renpho API to obtain a session key.
        """
        if not self.email or not self.password:
            raise Exception("Email and password must be provided")

        key = RSA.importKey(self.public_key)
        cipher = PKCS1_v1_5.new(key)
        encrypted_password = b64encode(cipher.encrypt(self.password.encode("utf-8")))

        data = {"secure_flag": 1, "email": self.email, "password": encrypted_password}
        parsed = self._request_sync("POST", API_AUTH_URL, data=data)

        if "terminal_user_session_key" not in parsed:
            raise AuthenticationError("Authentication failed")

        self.session_key = parsed["terminal_user_session_key"]
        return parsed

    async def auth(self):
        """
        Authenticate with the Renpho API to obtain a session key.
        """
        if not self.email or not self.password:
            raise AuthenticationError("Email and password must be provided")

        key = RSA.importKey(self.public_key)
        cipher = PKCS1_v1_5.new(key)
        encrypted_password = b64encode(cipher.encrypt(self.password.encode("utf-8")))

        data = {"secure_flag": "1", "email": self.email, "password": encrypted_password}
        parsed = await self._request("POST", API_AUTH_URL, json=data)

        if "terminal_user_session_key" not in parsed:
            raise AuthenticationError("Authentication failed")

        self.session_key = parsed["terminal_user_session_key"]
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

    def get_scale_users_sync(self):
        """
        Fetch the list of users associated with the scale.
        """
        url = f"{API_SCALE_USERS_URL}?locale=en&terminal_user_session_key={self.session_key}"
        parsed = self._request_sync("GET", url)
        self.set_user_id(parsed["scale_users"][0]["user_id"])
        return parsed["scale_users"]

    async def get_scale_users(self):
        """
        Fetch the list of users associated with the scale.
        """
        try:
            url = f"{API_SCALE_USERS_URL}?locale=en&terminal_user_session_key={self.session_key}"
            parsed = await self._request("GET", url)

            if not parsed or "scale_users" not in parsed:
                _LOGGER.warning(
                    "Invalid response or 'scale_users' not in the response."
                )
                return None

            self.set_user_id(parsed["scale_users"][0]["user_id"])
            return parsed["scale_users"]
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Aiohttp client error: {e}")
        except Exception as e:
            _LOGGER.error(f"An unexpected error occurred: {e}")
        return None

    def get_measurements_sync(self) -> Optional[List[Dict]]:
        """
        Fetch the most recent weight measurements for the user.
        """
        try:
            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=7)
            week_ago_timestamp = int(time.mktime(week_ago.timetuple()))
            url = f"{API_MEASUREMENTS_URL}?user_id={self.user_id}&last_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
            parsed = self._request_sync("GET", url)

            if "last_ary" not in parsed:
                _LOGGER.warning(f"Field 'last_ary' is not in the response: {parsed}")
                return None

            last_measurement = parsed["last_ary"][0]
            self.weight = last_measurement.get("weight", None)
            self.time_stamp = last_measurement.get("time_stamp", None)
            return parsed["last_ary"]
        except Exception as e:
            _LOGGER.error(f"An error occurred: {e}")
            return None

    async def get_measurements(self) -> Optional[List[Dict]]:
        """
        Fetch the most recent weight measurements for the user.
        """
        try:
            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=7)
            week_ago_timestamp = int(time.mktime(week_ago.timetuple()))
            url = f"{API_MEASUREMENTS_URL}?user_id={self.user_id}&last_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
            parsed = await self._request("GET", url)

            if not parsed or "last_ary" not in parsed:
                _LOGGER.warning("Invalid response or 'last_ary' not in the response.")
                return None

            last_measurement = parsed["last_ary"][0]
            self.weight = last_measurement.get("weight", None)
            self.time_stamp = last_measurement.get("time_stamp", None)
            return parsed["last_ary"]
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Aiohttp client error: {e}")
        except Exception as e:
            _LOGGER.error(f"An unexpected error occurred: {e}")
        return None

    def get_specific_metric_sync(
        self, metric_type: str, metric: str, user_id: Optional[str] = None
    ) -> Optional[float]:
        """
        Synchronous version of get_specific_metric based on the type specified (weight, growth goal, or growth metric).

        Parameters:
            metric_type (str): The type of metric to fetch ('weight', 'growth_goal', 'growth').
            metric (str): The specific metric to fetch (e.g., "height", "growth_rate", "weight").
            user_id (str, optional): The user ID for whom to fetch the metric. Defaults to None.

        Returns:
            float, None: The fetched metric value, or None if it couldn't be fetched.
        """
        try:
            if user_id:
                self.set_user_id(user_id)  # Update the user_id if provided

            if metric_type == "weight":
                last_measurement = self.get_measurements_sync()
                return (
                    last_measurement[0].get(metric, None) if last_measurement else None
                )

            elif metric_type == "growth_goal":
                growth_goal_info = self.list_growth_goal_sync()
                last_goal = (
                    growth_goal_info.get("growth_goals", [])[0]
                    if growth_goal_info.get("growth_goals")
                    else None
                )
                return last_goal.get(metric, None) if last_goal else None

            elif metric_type == "growth":
                growth_info = self.list_growth_sync()
                last_measurement = (
                    growth_info.get("growths", [])[0]
                    if growth_info.get("growths")
                    else None
                )
                return last_measurement.get(metric, None) if last_measurement else None

            else:
                _LOGGER.error(
                    "Invalid metric_type. Must be 'weight', 'growth_goal', or 'growth'."
                )
                return None

        except Exception as e:
            _LOGGER.error(f"An error occurred: {e}")
            return None

    async def get_specific_metric(
        self, metric_type: str, metric: str, user_id: Optional[str] = None
    ) -> Optional[float]:
        """
        Fetch a specific metric based on the type specified (weight, growth goal, or growth metric).

        Parameters:
            metric_type (str): The type of metric to fetch ('weight', 'growth_goal', 'growth').
            metric (str): The specific metric to fetch (e.g., "height", "growth_rate", "weight").
            user_id (str, optional): The user ID for whom to fetch the metric. Defaults to None.

        Returns:
            float, None: The fetched metric value, or None if it couldn't be fetched.
        """
        try:
            if user_id:
                self.set_user_id(user_id)  # Update the user_id if provided

            if metric_type == "weight":
                last_measurement = await self.get_measurements()
                return (
                    last_measurement[0].get(metric, None) if last_measurement else None
                )

            elif metric_type == "growth_goal":
                growth_goal_info = await self.list_growth_goal()
                last_goal = (
                    growth_goal_info.get("growth_goals", [])[0]
                    if growth_goal_info.get("growth_goals")
                    else None
                )
                return last_goal.get(metric, None) if last_goal else None
            elif metric_type == "growth":
                growth_info = await self.list_growth()
                last_measurement = (
                    growth_info.get("growths", [])[0]
                    if growth_info.get("growths")
                    else None
                )
                return last_measurement.get(metric, None) if last_measurement else None
            else:
                print(
                    "Invalid metric_type. Must be 'weight', 'growth_goal', or 'growth'."
                )
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    async def get_specific_metric_from_user_ID(
        self, metric_type: str, metric: str, user_id: Optional[str] = None
    ) -> Optional[float]:
        """
        Fetch a specific metric for a particular user ID based on the type specified (weight, growth goal, or growth metric).

        Parameters:
            metric_type (str): The type of metric to fetch ('weight', 'growth_goal', 'growth').
            metric (str): The specific metric to fetch (e.g., "height", "growth_rate", "weight").
            user_id (str, optional): The user ID for whom to fetch the metric. Defaults to None.

        Returns:
            float, None: The fetched metric value, or None if it couldn't be fetched.
        """
        try:
            if user_id:
                self.set_user_id(user_id)  # Update the user_id if provided

            if metric_type == "weight":
                last_measurement = await self.get_measurements()
                return (
                    last_measurement[0].get(metric, None) if last_measurement else None
                )

            elif metric_type == "growth_goal":
                growth_goal_info = await self.list_growth_goal()
                last_goal = (
                    growth_goal_info.get("growth_goals", [])[0]
                    if growth_goal_info.get("growth_goals")
                    else None
                )
                return last_goal.get(metric, None) if last_goal else None

            elif metric_type == "growth":
                growth_info = await self.list_growth()
                last_measurement = (
                    growth_info.get("growths", [])[0]
                    if growth_info.get("growths")
                    else None
                )
                return last_measurement.get(metric, None) if last_measurement else None

            else:
                print(
                    "Invalid metric_type. Must be 'weight', 'growth_goal', or 'growth'."
                )
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_info_sync(self):
        """
        Wrapper method to authenticate, fetch users, and get measurements.
        """
        self.auth_sync()
        self.get_scale_users_sync()
        self.get_measurements_sync()
        return self.get_measurements_sync()

    async def get_info(self):
        """
        Wrapper method to authenticate, fetch users, and get measurements.
        """
        await self.auth()
        await self.get_scale_users()
        return await self.get_measurements()

    async def start_polling(self, polling_interval=60):
        """
        Start polling for weight data at a given interval.
        """
        await self.get_info()
        polling_interval = polling_interval if polling_interval > 0 else 60
        while True:
            await asyncio.sleep(self.refresh)
            await self.get_info()

    def stop_polling(self):
        """
        Stop polling for weight data.
        """
        if hasattr(self, "polling"):
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

    async def get_device_info(self):
        """
        Asynchronously get device information.
        Returns:
            dict: The API response as a dictionary.
        """
        week_ago_timestamp = self.get_week_ago_timestamp()
        url = f"{DEVICE_INFO_URL}?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        return await self._request("GET", url)

    async def list_latest_model(self):
        """
        Asynchronously list the latest model information.

        Returns:
            dict: The API response as a dictionary.
        """
        week_ago_timestamp = self.get_week_ago_timestamp()
        url = f"{LATEST_MODEL_URL}?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        return await self._request("GET", url)

    async def list_girth(self):
        """
        Asynchronously list girth information.

        Returns:
            dict: The API response as a dictionary.
        """
        week_ago_timestamp = self.get_week_ago_timestamp()
        url = f"{GIRTH_URL}?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        return await self._request("GET", url)

    async def list_girth_goal(self):
        """
        Asynchronously list girth goal information.

        Returns:
            dict: The API response as a dictionary.
        """
        week_ago_timestamp = self.get_week_ago_timestamp()
        url = f"{GIRTH_GOAL_URL}?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        return await self._request("GET", url)

    async def get_specific_growth_goal_metric(
        self, metric: str, user_id: Optional[str] = None
    ) -> Optional[float]:
        """
        Fetch a specific growth goal metric for a particular user ID from the most recent growth goal information.

        Parameters:
            metric (str): The specific metric to fetch (e.g., "height_goal", "growth_rate_goal").
            user_id (str, optional): The user ID for whom to fetch the metric. Defaults to None.

        Returns:
            float, None: The fetched metric value, or None if it couldn't be fetched.
        """
        try:
            if user_id:
                self.set_user_id(user_id)  # Update the user_id if provided
            growth_goal_info = await self.list_growth_goal()
            last_goal = (
                growth_goal_info.get("growth_goals", [])[0]
                if growth_goal_info.get("growth_goals")
                else None
            )
            return last_goal.get(metric, None) if last_goal else None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    async def list_growth_record(self):
        """
        Asynchronously list growth records.
        Returns:
            dict: The API response as a dictionary.
        """
        week_ago_timestamp = self.get_week_ago_timestamp()
        url = f"https://renpho.qnclouds.com/api/v3/growth_records/list_growth_record.json?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        return await self._request("GET", url)

    async def get_specific_growth_metric(
        self, metric: str, user_id: Optional[str] = None
    ) -> Optional[float]:
        """
        Fetch a specific growth metric for a particular user ID from the most recent growth measurement.

        Parameters:
            metric (str): The specific metric to fetch (e.g., "height", "growth_rate").
            user_id (str, optional): The user ID for whom to fetch the metric. Defaults to None.

        Returns:
            float, None: The fetched metric value, or None if it couldn't be fetched.
        """
        try:
            if user_id:
                self.set_user_id(user_id)  # Update the user_id if provided
            growth_info = await self.list_growth()
            last_measurement = (
                growth_info.get("growths", [])[0]
                if growth_info.get("growths")
                else None
            )
            return last_measurement.get(metric, None) if last_measurement else None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    async def message_list(self):
        week_ago_timestamp = self.get_week_ago_timestamp()
        url = f"https://renpho.qnclouds.com/api/v2/messages/list.json?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        return await self._request("GET", url)

    async def close(self):
        """
        Shutdown the executor when you are done using the RenphoWeight instance.
        """
        await self.session.close()
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


class AuthenticationError(Exception):
    pass


class APIError(Exception):
    pass
