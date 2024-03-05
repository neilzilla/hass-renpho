from fastapi import FastAPI, Request, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os

import asyncio
import datetime
import logging
import time
from base64 import b64encode
from threading import Timer
from typing import Callable, Dict, Final, List, Optional, Union, Any
from contextlib import asynccontextmanager

import aiohttp
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from pydantic import BaseModel
import logging


METRIC_TYPE_WEIGHT: Final = "weight"
METRIC_TYPE_GROWTH_RECORD: Final = "growth_record"
METRIC_TYPE_GIRTH: Final = "girth"
METRIC_TYPE_GIRTH_GOAL: Final = "girth_goals"

CONF_PUBLIC_KEY: Final = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+25I2upukpfQ7rIaaTZtVE744
u2zV+HaagrUhDOTq8fMVf9yFQvEZh2/HKxFudUxP0dXUa8F6X4XmWumHdQnum3zm
Jr04fz2b2WCcN0ta/rbF2nYAnMVAk2OJVZAMudOiMWhcxV1nNJiKgTNNr13de0EQ
IiOL2CUBzu+HmIfUbQIDAQAB
-----END PUBLIC KEY-----"""


# Initialize logging
_LOGGER = logging.getLogger(__name__)

# API Endpoints
API_AUTH_URL = "https://renpho.qnclouds.com/api/v3/users/sign_in.json?app_id=Renpho" # Authentication Post
API_SCALE_USERS_URL = "https://renpho.qnclouds.com/api/v3/scale_users/list_scale_user" # Scale users
API_MEASUREMENTS_URL = "https://renpho.qnclouds.com/api/v2/measurements/list.json" # Measurements
DEVICE_INFO_URL = "https://renpho.qnclouds.com/api/v2/device_binds/get_device.json" # Device info
LATEST_MODEL_URL = "https://renpho.qnclouds.com/api/v3/devices/list_lastest_model.json" # Latest model
GIRTH_URL = "https://renpho.qnclouds.com/api/v3/girths/list_girth.json" # Girth
GIRTH_GOAL_URL = "https://renpho.qnclouds.com/api/v3/girth_goals/list_girth_goal.json" # Girth goal
GROWTH_RECORD_URL = "https://renpho.qnclouds.com/api/v3/growth_records/list_growth_record.json" # Growth record
MESSAGE_LIST_URL = "https://renpho.qnclouds.com/api/v2/messages/list.json" # message to support
USER_REQUEST_URL = "https://renpho.qnclouds.com/api/v2/users/request_user.json" # error
USERS_REACH_GOAL = "https://renpho.qnclouds.com/api/v3/users/reach_goal.json" # error 404


from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel

class DeviceBind(BaseModel):
    id: int
    mac: str
    scale_name: str
    demo: str
    hw_ble_version: int
    device_type: int
    hw_software_version: int
    created_at: str
    uuid: str
    b_user_id: int
    internal_model: str
    wifi_name: str
    product_category: int

    def get(self, key, default=None):
        return getattr(self, key, default)

class UserResponse(BaseModel):
    status_code: str
    status_message: str
    terminal_user_session_key: str
    device_binds_ary: List[DeviceBind]
    new_bodyage_logic_flag: int
    cooling_period_flag: int
    id: int
    email: str
    account_name: str
    gender: int
    height: float
    height_unit: int
    waistline: int
    hip: int
    person_type: int
    category_type: int
    weight_unit: int
    current_goal_weight: float
    weight_goal_unit: int
    weight_goal: float
    locale: str
    birthday: str
    weight_goal_date: str
    avatar_url: str
    weight: float
    facebook_account: str
    twitter_account: str
    line_account: str
    sport_goal: int
    sleep_goal: int
    bodyfat_goal: float
    initial_weight: float
    initial_bodyfat: float
    area_code: str
    method: int
    user_code: str
    agree_flag: int
    reach_goal_weight_flag: int
    reach_goal_bodyfat_flag: int
    set_goal_at: int
    sell_flag: int
    allow_notification_flag: int
    phone: str
    region_code: str
    dump_flag: int
    weighing_mode: int
    password_present_flag: int
    stature: float
    custom: str
    index_extension: int
    person_body_shape: int
    person_goal: int
    accuracy_flag: int

    def get(self, key, default=None):
        return getattr(self, key, default)

class MeasurementDetail(BaseModel):
    id: int
    b_user_id: int
    time_stamp: int
    created_at: str
    created_stamp: int
    scale_type: int
    scale_name: str
    mac: str
    gender: int
    height: int
    height_unit: int
    birthday: str
    category_type: int
    person_type: int
    weight: float
    bodyfat: Optional[float] = None
    water: Optional[float] = None
    bmr: Optional[int] = None
    weight_unit: int
    bodyage: Optional[int] = None
    muscle: Optional[float] = None
    bone: Optional[float] = None
    subfat: Optional[float] = None
    visfat: Optional[int] = None
    bmi: float
    sinew: Optional[float] = None
    protein: Optional[float] = None
    body_shape: int
    fat_free_weight: Optional[float] = None
    resistance: Optional[int] = None
    sec_resistance: Optional[int] = None
    internal_model: str
    actual_resistance: Optional[int] = None
    actual_sec_resistance: Optional[int] = None
    heart_rate: Optional[int] = None
    cardiac_index: Optional[int] = None
    method: int
    sport_flag: int
    left_weight: Optional[float] = None
    waistline: Optional[float] = None
    hip: Optional[float] = None
    local_created_at: str
    time_zone: Optional[str] = None
    right_weight: Optional[float] = None
    accuracy_flag: int
    bodyfat_left_arm: Optional[float] = None
    bodyfat_left_leg: Optional[float] = None
    bodyfat_right_leg: Optional[float] = None
    bodyfat_right_arm: Optional[float] = None
    bodyfat_trunk: Optional[float] = None
    sinew_left_arm: Optional[float] = None
    sinew_left_leg: Optional[float] = None
    sinew_right_arm: Optional[float] = None
    sinew_right_leg: Optional[float] = None
    sinew_trunk: Optional[float] = None
    resistance20_left_arm: Optional[int] = None
    resistance20_left_leg: Optional[int] = None
    resistance20_right_leg: Optional[int] = None
    resistance20_right_arm: Optional[int] = None
    resistance20_trunk: Optional[int] = None
    resistance100_left_arm: Optional[int] = None
    resistance100_left_leg: Optional[int] = None
    resistance100_right_arm: Optional[int] = None
    resistance100_right_leg: Optional[int] = None
    resistance100_trunk: Optional[int] = None
    remark: Optional[str] = None
    score: Optional[int] = None
    pregnant_flag: Optional[int] = None
    stature: Optional[int] = None
    category: Optional[int] = None
    sea_waist: Optional[float] = None
    sea_hip: Optional[float] = None
    sea_whr_value: Optional[float] = None
    sea_chest: Optional[float] = None
    sea_abdomen: Optional[float] = None
    sea_neck: Optional[float] = None
    sea_left_arm: Optional[float] = None
    sea_right_arm: Optional[float] = None
    sea_left_thigh: Optional[float] = None
    sea_right_thigh: Optional[float] = None
    origin_resistances: Optional[str] = None

    def get(self, key, default=None):
        return getattr(self, key, default)


class MeasurementResponse(BaseModel):
    status_code: str
    status_message: str
    last_at: int
    previous_flag: int
    previous_at: int
    measurements: List[MeasurementDetail]

    def get(self, key, default=None):
        return getattr(self, key, default)


class Users(BaseModel):
    scale_user_id: str
    user_id: str
    mac: str
    index: int
    key: int
    method: int
    def get(self, key, default=None):
        return getattr(self, key, default)

class GirthGoal(BaseModel):
    girth_goal_id: int
    user_id: int
    girth_type: str
    setup_goal_at: int
    goal_value: float
    goal_unit: int
    initial_value: float
    initial_unit: int
    finish_goal_at: int
    finish_value: float
    finish_unit: int

    def get(self, key, default=None):
        return getattr(self, key, default)

class GirthGoalsResponse(BaseModel):
    status_code: str
    status_message: str
    terminal_user_session_key: str
    girth_goals: List[GirthGoal]
    new_bodyage_logic_flag: int
    cooling_period_flag: int
    id: int
    email: str
    account_name: str
    gender: int
    height: float
    height_unit: int
    waistline: int
    hip: int
    person_type: int
    category_type: int
    weight_unit: int
    current_goal_weight: float
    weight_goal_unit: int
    weight_goal: float
    locale: str
    birthday: str
    weight_goal_date: str
    avatar_url: str
    weight: float
    facebook_account: str
    twitter_account: str
    line_account: str
    sport_goal: int
    sleep_goal: int
    bodyfat_goal: float
    initial_weight: float
    initial_bodyfat: float
    area_code: str
    method: int
    user_code: str
    agree_flag: int
    reach_goal_weight_flag: int
    reach_goal_bodyfat_flag: int
    set_goal_at: int
    sell_flag: int
    allow_notification_flag: int
    phone: str
    region_code: str
    dump_flag: int
    weighing_mode: int
    password_present_flag: int
    stature: float
    custom: str
    index_extension: int
    person_body_shape: int
    person_goal: int
    accuracy_flag: int

    def get(self, key, default=None):
        return getattr(self, key, default)

class Girth(BaseModel):
    girth_id: int
    user_id: int
    time_stamp: int
    time_zone: str
    mac: str
    internal_model: str
    scale_name: str
    neck_value: float
    neck_unit: int
    shoulder_value: float
    shoulder_unit: int
    arm_value: float
    arm_unit: int
    chest_value: float
    chest_unit: int
    waist_value: float
    waist_unit: int
    hip_value: float
    hip_unit: int
    thigh_value: float
    thigh_unit: int
    calf_value: float
    calf_unit: int
    left_arm_value: float
    left_arm_unit: int
    left_thigh_value: float
    left_thigh_unit: int
    left_calf_value: float
    left_calf_unit: int
    right_arm_value: float
    right_arm_unit: int
    right_thigh_value: float
    right_thigh_unit: int
    right_calf_value: float
    right_calf_unit: int
    whr_value: float
    abdomen_value: float
    abdomen_unit: int
    custom: str
    custom_value: float
    custom_unit: int
    updated_at: int
    custom1: str
    custom_value1: float
    custom_unit1: int
    custom2: str
    custom_value2: float
    custom_unit2: int
    custom3: str
    custom_value3: float
    custom_unit3: int
    custom4: str
    custom_value4: float
    custom_unit4: int
    custom5: str
    custom_value5: float
    custom_unit5: int

    def get(self, key, default=None):
        return getattr(self, key, default)

class GirthResponse(BaseModel):
    status_code: str
    status_message: str
    terminal_user_session_key: str
    girths: List[Girth]
    deleted_girth_ids: List[int]
    last_updated_at: int

    def get(self, key, default=None):
        return getattr(self, key, default)


class RenphoWeight:
    """
    A class to interact with Renpho's weight scale API.

    Attributes:
        email (str): The email address for the Renpho account.
        password (str): The password for the Renpho account.
        user_id (str, optional): The ID of the user for whom weight data should be fetched.
    """

    def __init__(self, email, password, user_id=None, refresh=60):
        """Initialize a new RenphoWeight instance."""
        self.public_key: str = CONF_PUBLIC_KEY
        self.email: str = email
        self.password: str = password
        if user_id == "":
            user_id = None
        self.user_id: str = user_id
        self.refresh = refresh
        self.token: str = None
        self.session = None
        self.polling = False
        self.login_data: Optional[UserResponse] = None
        self.users: List[Users] = []
        self.weight_info: Optional[MeasurementDetail] = None
        self.weight_history: List[MeasurementDetail] = []
        self.weight: float = None
        self.weight_goal = {}
        self.device_info: Optional[List[DeviceBind]] = None
        self.latest_model: Optional[Dict] = None
        self.girth_info: Optional[Dict] = None
        self.girth_goal: Optional[Dict] = None
        self.growth_record: Optional[Dict] = None
        self._last_updated = None
        self._last_updated_weight = None
        self._last_updated_girth = None
        self._last_updated_girth_goal = None
        self._last_updated_growth_record = None
        self.auth_in_progress = False
        self.is_polling_active = False

    @staticmethod
    def get_timestamp() -> int:
        start_date = datetime.date(1998, 1, 1)
        return int(time.mktime(start_date.timetuple()))


    def prepare_data(self, data):
        if isinstance(data, bytes):
            return data.decode("utf-8")
        elif isinstance(data, dict):
            return {key: self.prepare_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.prepare_data(element) for element in data]
        else:
            return data

    async def open_session(self):
        """
        Open a new aiohttp session if one does not exist or is closed.
        """
        if self.session is None or self.session.closed:
            self.token = None
            self.session = aiohttp.ClientSession(
                headers={"Content-Type": "application/json", "Accept": "application/json"}
            )
        if self.session:
            self.session.close()
            self.session = None

    async def _request(self, method: str, url: str, retries: int = 3, skip_auth=False, **kwargs):
        """
        Perform an API request and return the parsed JSON response.

        Parameters:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            url (str): The URL to which the request should be made.
            retries (int, optional): The number of times to retry the request if it fails. Defaults to 3.
            skip_auth (bool, optional): Whether to skip authentication. Defaults to False.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            Union[Dict, List]: The parsed JSON response from the API request.
        """

        if retries < 1:
            _LOGGER.error("Max retries exceeded for API request.")
            raise APIError("Max retries exceeded for API request.")

        await self.open_session()

        if not self.token and not url.endswith("sign_in.json") and not skip_auth:
            auth_success = await self.auth()
            if not auth_success:
                raise AuthenticationError("Authentication failed. Unable to proceed with the request.")

        kwargs = self.prepare_data(kwargs)

        _LOGGER.error(f"API request: {method} {url} {kwargs}")

        try:
            async with self.session.request(method, url, **kwargs) as response:
                response.raise_for_status()
                parsed_response = await response.json()

                if parsed_response.get("status_code") == "40302":
                    self.token = None
                if parsed_response.get("status_code") == "50000":
                    raise APIError(f"Internal server error: {parsed_response.get('status_message')}")
                if parsed_response.get("status_code") == "20000" and parsed_response.get("status_message") == "ok":
                    return parsed_response
                else:
                    raise APIError(f"API request failed {method} {url}: {parsed_response.get('status_message')}")
        except (aiohttp.ClientResponseError, aiohttp.ClientConnectionError) as e:
            _LOGGER.error(f"Client error: {e}")
            raise APIError(f"API request failed {method} {url}") from e

    @staticmethod
    def encrypt_password(public_key_str, password):
        try:
            rsa_key = RSA.importKey(public_key_str)
            cipher = PKCS1_v1_5.new(rsa_key)
            return b64encode(cipher.encrypt(password.encode("utf-8"))).decode("utf-8")
        except Exception as e:
            _LOGGER.error(f"Encryption error: {e}")
            raise

    async def is_valid_session(self):
        """Check if the session key is valid."""
        return self.token is not None

    async def validate_credentials(self):
        """
        Validate the current credentials by attempting to authenticate.
        Returns True if authentication succeeds, False otherwise.
        """
        try:
            return await self.auth()
        except Exception as e:
            _LOGGER.error(f"Validation failed: {e}")
            return False

    async def auth(self):
        """Authenticate with the Renpho API."""

        if self.auth_in_progress:
            return False  # Avoid re-entry if already in progress

        self.auth_in_progress = True

        if not self.email or not self.password:
            raise AuthenticationError("Email and password are required for authentication.")

        if self.public_key is None:
            _LOGGER.error("Public key is None.")
            raise AuthenticationError("Public key is None.")

        encrypted_password = self.encrypt_password(self.public_key, self.password)

        data = {"secure_flag": "1", "email": self.email,
                "password": encrypted_password}

        _LOGGER.error(f"Authentication data: {data}")

        try:

            parsed = await self._request("POST", API_AUTH_URL, json=data, skip_auth=True)

            _LOGGER.warning(f"Authentication response: {parsed}")

            if parsed is None:
                _LOGGER.error("Authentication failed. No response received.")
                raise AuthenticationError("Authentication failed. No response received.")

            if parsed.get("status_code") == "50000" and parsed.get("status_message") == "Email was not registered":
                _LOGGER.warning("Email was not registered.")
                raise AuthenticationError("Email was not registered.")

            if parsed.get("status_code") == "500" and parsed.get("status_message") == "Internal Server Error":
                _LOGGER.warning("Bad Password or Internal Server Error.")
                raise AuthenticationError("Bad Password or Internal Server Error.")

            if "terminal_user_session_key" not in parsed:
                _LOGGER.error(
                    "'terminal_user_session_key' not found in parsed object.")
                raise AuthenticationError(f"Authentication failed: {parsed}")

            if parsed.get("status_code") == "20000" and parsed.get("status_message") == "ok":
                if 'terminal_user_session_key' in parsed:
                    self.session_key = parsed["terminal_user_session_key"]
                else:
                    self.session_key = None
                    raise AuthenticationError("Session key not found in response.")
                if 'device_binds_ary' in parsed:
                    parsed['device_binds_ary'] = [DeviceBind(**device) for device in parsed['device_binds_ary']]
                else:
                    parsed['device_binds_ary'] = []
                self.login_data = UserResponse(**parsed)
                if self.user_id is None:
                    self.user_id = self.login_data.get("id", None)
                return True
        except Exception as e:
            _LOGGER.error(f"Authentication failed: {e}")
            raise AuthenticationError("Authentication failed due to an error. {e}") from e
        finally:
            self.auth_in_progress = False

    async def get_scale_users(self) -> List[Users]:
        """
        Fetch the list of users associated with the scale.
        """
        url = f"{API_SCALE_USERS_URL}?user_id={self.user_id}&last_updated_at={self.get_timestamp()}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        # Perform the API request
        try:
            parsed = await self._request("GET", url, skip_auth=True)

            if not parsed:
                _LOGGER.error("Failed to fetch scale users.")
                return []

            # Check if the response is valid and contains 'scale_users'
            if "scale_users" in parsed:
                # Update the 'users' attribute with parsed and validated ScaleUser objects
                self.users = [Users(**user) for user in parsed["scale_users"]]
            else:
                _LOGGER.error("Failed to fetch scale users or no scale users found in the response.")

            self.user_id = self.users[0]["user_id"]
            return self.users
        except Exception as e:
            _LOGGER.error(f"Failed to fetch scale users: {e}")
            return []

    async def get_measurements(self):
        """
        Fetch the most recent weight measurements for the user.
        """
        url = f"{API_MEASUREMENTS_URL}?user_id={self.user_id}&last_at={self.get_timestamp()}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            parsed = await self._request("GET", url, skip_auth=True)

            if not parsed:
                _LOGGER.error("Failed to fetch weight measurements.")
                return

            if "status_code" in parsed and parsed["status_code"] == "20000":
                if "last_ary" not in parsed:
                    _LOGGER.error("No weight measurements found in the response.")
                    return
                if measurements := parsed["last_ary"]:
                    self.weight_history = [MeasurementDetail(**measurement) for measurement in measurements]
                    self.weight_info = self.weight_history[0] if self.weight_history else None
                    self.weight = self.weight_info.weight if self.weight_info else None
                    self.time_stamp = self.weight_info.time_stamp if self.weight_info else None
                    self._last_updated_weight = time.time()
                    return self.weight_info
                else:
                    _LOGGER.error("No weight measurements found in the response.")
                    return None
            else:
                # Handling different error scenarios
                if "status_code" not in parsed:
                    _LOGGER.error("Invalid response format received from weight measurements endpoint.")
                else:
                    _LOGGER.error(f"Error fetching weight measurements: Status Code {parsed.get('status_code')} - {parsed.get('status_message')}")
                return None

        except Exception as e:
            _LOGGER.error(f"Failed to fetch weight measurements: {e}")
            return None

    async def get_weight(self) -> Union[float, None]:
        if self.weight and self.weight_info:
            return self.weight, self.weight_info
        self._last_updated_weight = time.time()
        return self.weight, await self.get_measurements()

    async def get_info(self):
        self._last_updated_weight = time.time()
        return await self.get_measurements()

    async def get_device_info(self) -> Optional[List[DeviceBind]]:
        """
        Fetch device information and update the class attribute with device bind details.
        """
        url = f"{DEVICE_INFO_URL}?user_id={self.user_id}&last_updated_at={self.get_timestamp()}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            parsed = await self._request("GET", url, skip_auth=True)

            if not parsed:
                _LOGGER.error("Failed to fetch device info.")
                return None

            # Check for successful response code
            if parsed.get("status_code") == "20000" and "device_binds_ary" in parsed:
                device_info = [DeviceBind(**device) for device in parsed["device_binds_ary"]]
                self.device_info = device_info
                return device_info
            else:
                # Handling different error scenarios
                if "status_code" not in parsed or "device_binds_ary" not in parsed:
                    _LOGGER.error("Invalid response format received from device info endpoint.")
                else:
                    _LOGGER.error(f"Error fetching device info: Status Code {parsed.get('status_code')} - {parsed.get('status_message')}")
                return None
        except Exception as e:
            _LOGGER.error(f"Failed to fetch device info: {e}")
            return None

    async def list_latest_model(self):
        """
        Fetch the latest model for the user.
        """
        url = f"{LATEST_MODEL_URL}?user_id={self.user_id}&last_updated_at={self.get_timestamp()}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}$internal_model_json=%5B%22{self.login_data.internal_model}%22%5D"
        try:
            parsed = await self._request("GET", url, skip_auth=True)

            if not parsed:
                _LOGGER.error("Failed to fetch latest model.")
                return None

            if "status_code" in parsed and parsed["status_code"] == "20000":
                self.latest_model = parsed
                return parsed
            else:
                _LOGGER.error(f"Error fetching latest model: {parsed.get('status_message')}")
                return None
        except Exception as e:
            _LOGGER.error(f"Failed to fetch latest model: {e}")
            return None

    async def list_girth(self) -> Optional[dict]:
        url = f"{GIRTH_URL}?user_id={self.user_id}&last_updated_at={self.get_timestamp()}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            parsed = await self._request("GET", url, skip_auth=True)

            if not parsed:
                _LOGGER.error("Failed to fetch girth info.")
                return None

            if "status_code" in parsed and parsed["status_code"] == "20000":
                response = GirthResponse(**parsed)
                self.girth_info = response.get("girths", {})
                return parsed
            else:
                _LOGGER.error(f"Error fetching girth info: {parsed.get('status_message')}")
                return None

        except Exception as e:
            _LOGGER.error(f"Failed to fetch girth info: {e}")
            return None

    async def list_girth_goal(self):
        """
        Fetch the girth goal for the user.
        """
        url = f"{GIRTH_GOAL_URL}?user_id={self.user_id}&last_updated_at={self.get_timestamp()}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            parsed = await self._request("GET", url, skip_auth=True)

            if not parsed:
                _LOGGER.error("Failed to fetch girth goal.")
                return None

            if "status_code" in parsed and parsed["status_code"] == "20000":
                response = GirthGoalsResponse(**parsed)
                self.girth_goal = GirthGoal(**response.get("girth_goals", {}))
                self._last_updated_girth_goal = time.time()
                return parsed
            else:
                _LOGGER.error(f"Error fetching girth goal: {parsed.get('status_message')}")
                return None
        except Exception as e:
            _LOGGER.error(f"Failed to fetch girth goal: {e}")
            return None

    async def list_growth_record(self):
        """
        Fetch the growth record for the user.
        """

        url = f"{GROWTH_RECORD_URL}?user_id={self.user_id}&last_updated_at={self.get_timestamp()}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            parsed = await self._request("GET", url, skip_auth=True)

            if not parsed:
                _LOGGER.error("Failed to fetch growth record.")
                return None

            if "status_code" in parsed and parsed["status_code"] == "20000":
                self.growth_record = parsed
                self._last_updated_growth_record = time.time()
                return parsed
            else:
                _LOGGER.error(f"Error fetching growth record: {parsed.get('status_message')}")
                return None
        except Exception as e:
            _LOGGER.error(f"Failed to fetch growth record: {e}")
            return None

    async def message_list(self):
        """
        Asynchronously list messages.
        """
        url = f"{MESSAGE_LIST_URL}?user_id={self.user_id}&last_updated_at={self.get_timestamp()}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            parsed = await self._request("GET", url, skip_auth=True)

            if not parsed:
                _LOGGER.error("Failed to fetch messages.")
                return None

            if "status_code" in parsed and parsed["status_code"] == "20000":
                return parsed
            _LOGGER.error(f"Error fetching messages: {parsed.get('status_message')}")
            return None
        except Exception as e:
            _LOGGER.error(f"Failed to fetch messages: {e}")
            return None

    async def request_user(self):
        """
        Asynchronously request user
        """
        url = f"{USER_REQUEST_URL}?user_id={self.user_id}&last_updated_at={self.get_timestamp()}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            parsed = await self._request("GET", url, skip_auth=True)

            if not parsed:
                _LOGGER.error("Failed to request user.")
                return None

            if "status_code" in parsed and parsed["status_code"] == "20000":
                return parsed
            _LOGGER.error(f"Error requesting user: {parsed.get('status_message')}")
            return None
        except Exception as e:
            _LOGGER.error(f"Failed to request user: {e}")
            return None

    async def reach_goal(self):
        """
        Asynchronously reach goal
        """

        url = f"{USERS_REACH_GOAL}?user_id={self.user_id}&last_updated_at={self.get_timestamp()}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            parsed = await self._request("GET", url, skip_auth=True)

            if not parsed:
                _LOGGER.error("Failed to reach goal.")
                return None

            if "status_code" in parsed and parsed["status_code"] == "20000":
                return parsed
            _LOGGER.error(f"Error reaching goal: {parsed.get('status_message')}")
            return None
        except Exception as e:
            _LOGGER.error(f"Failed to reach goal: {e}")
            return None

    async def get_specific_metric(self, metric_type: str, metric: str, user_id: Optional[str] = None):
        """
        Fetch a specific metric for a particular user ID based on the type specified.

        Parameters:
            metric_type (str): The type of metric to fetch.
            metric (str): The specific metric to fetch.
            user_id (Optional[str]): The user ID for whom to fetch the metric. Defaults to None.
        """


        if user_id:
            self.user_id = user_id

        try:
            if metric_type == METRIC_TYPE_WEIGHT:
                if self.weight_info:
                    return self.weight_info.get(metric, None)
                if self._last_updated_weight is None or time.time() - self._last_updated_weight > self.refresh:
                    last_measurement = await self.get_weight()
                    if last_measurement and self.weight is not None:
                        return last_measurement[1].get(metric, None) if last_measurement[1] else None
            elif metric_type == METRIC_TYPE_GIRTH:
                if not self.girth_info:
                    return await self.list_girth()
                if self._last_updated_girth is None or time.time() - self._last_updated_girth > self.refresh:
                    last_measurement = (
                        self.girth_info.get("girths", [])[0]
                        if self.girth_info.get("girths")
                        else None
                    )
                    return last_measurement.get(metric, None) if last_measurement else None
            elif metric_type == METRIC_TYPE_GIRTH_GOAL:
                if not self.girth_goal:
                    return await self.get_specific_girth_goal_metric(metric)
                last_goal = next(
                    (goal for goal in self.girth_goal['girth_goals'] if goal['girth_type'] == metric),
                    None
                )
                if self._last_updated_girth_goal is None or time.time() - self._last_updated_girth_goal > self.refresh:
                    return last_goal.get('goal_value', None)
            elif metric_type == METRIC_TYPE_GROWTH_RECORD:
                if not self.growth_record:
                    return await self.list_growth_record()
                if self._last_updated_growth_record is None or time.time() - self._last_updated_growth_record > self.refresh:
                    last_measurement = (
                        self.growth_record.get("growths", [])[0]
                        if self.growth_record.get("growths")
                        else None
                    )
                    return last_measurement.get(metric, None) if last_measurement else None
            else:
                _LOGGER.error(f"Invalid metric type: {metric_type}")
                return None
        except Exception as e:
            _LOGGER.error(f"Failed to fetch specific metric: {e}")
            return None

    async def get_specific_girth_goal_metric(self, metric: str, user_id: Optional[str] = None):
        """
        Fetch a specific girth goal metric for a particular user ID from the most recent girth goal information.

        Parameters:
            metric (str): The specific metric to fetch.
            user_id (str, optional): The user ID for whom to fetch the metric. Defaults to None.

        """
        try:
            if user_id:
                self.user_id = user_id
            if not self.girth_goal:
                await self.list_girth_goal()

            if self.girth_goal:
                last_goal = next(
                    (goal for goal in self.girth_goal['girth_goals'] if goal['girth_type'] == metric),
                    None
                )

                return last_goal.get('goal_value', None)
            else:
                return None
        except Exception as e:
            _LOGGER.error(f"Failed to fetch girth goal metric: {e}")
            return None

    async def get_specific_growth_metric(self, metric: str, user_id: Optional[str] = None):
        """
        Fetch a specific growth metric for a particular user ID from the most recent growth measurement.

        Parameters:
            metric (str): The specific metric to fetch (e.g., "height", "growth_rate").
            user_id (str, optional): The user ID for whom to fetch the metric. Defaults to None.
        """
        try:
            if user_id:
                self.user_id = user_id
            if not self.growth_record:
                await self.list_growth_record()

            if not self.growth_record:
                return None
            last_measurement = (
                self.growth_record.get("growths", [])[0]
                if self.growth_record.get("growths")
                else None
            )
            return last_measurement.get(metric, None) if last_measurement else None
        except Exception as e:
            _LOGGER.error(f"Failed to fetch growth metric: {e}")
            return None

    async def poll_data(self):
        """
        The core polling logic that fetches data and processes it.
        """
        try:
            asyncio.gather(
                await self.get_info(),
                await self.list_girth(),
                await self.list_girth_goal(),
            )

            _LOGGER.info("Data fetched successfully.")
        except Exception as e:
            _LOGGER.error(f"Error fetching data: {e}")

    async def start_polling(self):
        """
        Start the polling process.
        """
        if self.is_polling_active:
            _LOGGER.warning("Polling is already active.")
            return

        self.is_polling_active = True
        self.polling_task = asyncio.create_task(self.polling_loop())

    async def polling_loop(self):
        """
        The polling loop that runs until is_polling_active is False.
        """
        try:
            while self.is_polling_active:
                await self.poll_data()
                await asyncio.sleep(self.refresh_interval)
        except asyncio.CancelledError:
            _LOGGER.info("Polling task was cancelled.")
        except Exception as e:
            _LOGGER.error(f"Unexpected error in polling loop: {e}")
        finally:
            _LOGGER.info("Polling loop exited.")

    def stop_polling(self):
        """
        Stop the polling process.
        """
        if not self.is_polling_active:
            _LOGGER.warning("Polling is not active.")
            return

        if self.polling_task:
            self.polling_task.cancel()
            _LOGGER.info("Polling has been stopped.")
            self.is_polling_active = False
            self.polling_task = None

    async def close(self):
        """
        Clean up resources, stop polling, and close sessions.
        """
        self.stop_polling()
        if self.session:
            await self.session.close()
            _LOGGER.info("Aiohttp session closed")




class AuthenticationError(Exception):
    pass


class APIError(Exception):
    pass


class ClientSSLError(Exception):
    pass

# Initialize FastAPI and Jinja2
app = FastAPI(docs_url="/docs", redoc_url=None)

current_directory = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_directory, "templates"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()


class APIResponse(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    try:
        user = RenphoWeight(email=credentials.username, password=credentials.password)
        await user.auth()  # Ensure that user can authenticate
        return user
    except Exception as e:
        __LOGGER.error(f"Authentication failed: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed")


@app.get("/")
def read_root(request: Request):
    return "Renpho API"

@app.get("/auth", response_model=APIResponse)
async def auth(renpho: RenphoWeight = Depends(get_current_user)):
    # If this point is reached, authentication was successful
    return APIResponse(status="success", message="Authentication successful.")

@app.get("/info", response_model=APIResponse)
async def get_info(renpho: RenphoWeight = Depends(get_current_user)):
    try:
        info = await renpho.get_info()
        if info:
            return APIResponse(status="success", message="Fetched user info.", data=info)
        await renpho.close()
        return APIResponse(status="error", message="User info not found.")
    except Exception as e:
        _LOGGER.error(f"Error fetching user info: {e}")
        await renpho.close()
        return APIResponse(status="error", message="Failed to fetch user info.")

@app.get("/users", response_model=APIResponse)
async def get_scale_users(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        users = await renpho.get_scale_users()
        if users:
            return APIResponse(status="success", message="Fetched scale users.", data={"users": users})
        await renpho.close()
        raise HTTPException(status_code=404, detail="Users not found")
    except Exception as e:
        _LOGGER.error(f"Error fetching scale users: {e}")
        await renpho.close()
        return APIResponse(status="error", message=str(e))

@app.get("/measurements", response_model=APIResponse)
async def get_measurements(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        measurements = await renpho.get_measurements()
        if measurements:
            return APIResponse(status="success", message="Fetched measurements.", data={"measurements": measurements})
        await renpho.close()
        raise HTTPException(status_code=404, detail="Measurements not found")
    except Exception as e:
        await renpho.close()
        _LOGGER.error(f"Error fetching measurements: {e}")
        return APIResponse(status="error", message=str(e))

@app.get("/weight", response_model=APIResponse)
async def get_weight(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        weight = await renpho.get_weight()
        if weight:
            return APIResponse(status="success", message="Fetched weight.", data={"weight": weight})
        await renpho.close()
        raise HTTPException(status_code=404, detail="Weight not found")
    except Exception as e:
        await renpho.close()
        _LOGGER.error(f"Error fetching weight: {e}")
        return APIResponse(status="error", message=str(e))

@app.get("/specific_metric", response_model=APIResponse)
async def get_specific_metric(request: Request, metric: str, metric_id: str, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        specific_metric = await renpho.get_specific_metric(metric, metric_id)
        if specific_metric:
            return APIResponse(status="success", message=f"Fetched specific metric: {metric} {metric_id}.", data={metric: specific_metric})
        await renpho.close()
        raise HTTPException(status_code=404, detail=f"Specific metric {metric} {metric_id} not found")
    except Exception as e:
        await renpho.close()
        _LOGGER.error(f"Error fetching specific metric: {e}")
        return APIResponse(status="error", message=str(e))

@app.get("/device_info", response_model=APIResponse)
async def get_device_info(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        device_info = await renpho.get_device_info()
        if device_info:
            return APIResponse(status="success", message="Fetched device info.", data=device_info)
        await renpho.close()
        raise HTTPException(status_code=404, detail="Device info not found")
    except Exception as e:
        await renpho.close()
        _LOGGER.error(f"Error fetching device info: {e}")
        return APIResponse(status="error", message=str(e))

@app.get("/latest_model", response_model=APIResponse)
async def list_latest_model(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        latest_model = await renpho.list_latest_model()
        if latest_model:
            return APIResponse(status="success", message="Fetched latest model.", data=latest_model)
        await renpho.close()
        raise HTTPException(status_code=404, detail="Latest model not found")
    except Exception as e:
        await renpho.close()
        _LOGGER.error(f"Error fetching latest model: {e}")
        return APIResponse(status="error", message=str(e))

@app.get("/girth_info", response_model=APIResponse)
async def list_girth(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        girth_info = await renpho.list_girth()
        if girth_info:
            return APIResponse(status="success", message="Fetched girth info.", data=girth_info)
        await renpho.close()
        raise HTTPException(status_code=404, detail="Girth info not found")
    except Exception as e:
        await renpho.close()
        _LOGGER.error(f"Error fetching girth info: {e}")
        return APIResponse(status="error", message=str(e))

@app.get("/girth_goal", response_model=APIResponse)
async def list_girth_goal(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        girth_goal = await renpho.list_girth_goal()
        if girth_goal:
            return APIResponse(status="success", message="Fetched girth goal.", data=girth_goal)
        await renpho.close()
        raise HTTPException(status_code=404, detail="Girth goal not found")
    except Exception as e:
        await renpho.close()
        _LOGGER.error(f"Error fetching girth goal: {e}")
        return APIResponse(status="error", message=str(e))

@app.get("/growth_record", response_model=APIResponse)
async def list_growth_record(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        growth_record = await renpho.list_growth_record()
        if growth_record:
            return APIResponse(status="success", message="Fetched growth record.", data=growth_record)
        await renpho.close()
        raise HTTPException(status_code=404, detail="Growth record not found")
    except Exception as e:
        await renpho.close()
        _LOGGER.error(f"Error fetching growth record: {e}")
        return APIResponse(status="error", message=str(e))

@app.get("/message_list", response_model=APIResponse)
async def message_list(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        messages = await renpho.message_list()
        if messages:
            return APIResponse(status="success", message="Fetched message list.", data=messages)
        await renpho.close()
        raise HTTPException(status_code=404, detail="Message list not found")
    except Exception as e:
        await renpho.close()
        _LOGGER.error(f"Error fetching message list: {e}")
        return APIResponse(status="error", message=str(e))