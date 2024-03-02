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
from typing import Callable, Dict, Final, List, Optional, Union

import aiohttp
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


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
MESSAGE_LIST_URL = "https://renpho.qnclouds.com/api/v2/messages/list.json"
USER_REQUEST_URL = "https://renpho.qnclouds.com/api/v2/users/request_user.json"
USERS_REACH_GOAL = "https://renpho.qnclouds.com/api/v3/users/reach_goal.json"


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

    def __init__(self, email, password, public_key=CONF_PUBLIC_KEY, user_id=None, refresh=60):
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
            self.refresh = refresh
            self.session = None
            self.is_polling_active = False
            self.session_key_expiry = datetime.datetime.now()

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

    @staticmethod
    def get_ago_timestamp() -> int:
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
        if self.session is None or self.session.closed:
            self.session_key = None
            self.session_key_expiry = datetime.datetime.now()
            self.session = aiohttp.ClientSession()

    async def _request(self, method: str, url: str, **kwargs) -> Union[Dict, List]:
        """
        Asynchronous function to make API requests.

        Parameters:
            method (str): The HTTP method to use ('GET', 'POST', etc.)
            url (str): The URL to send the request to.
            **kwargs: Additional keyword arguments to pass to the aiohttp request.

        Returns:
            Union[Dict, List]: The parsed JSON response from the API as a dictionary or list.

        Raises:
            APIError: Custom exception for API-related errors.
        """
        try:
            # Initialize session if it does not exist
            await self.open_session()

            # Authenticate if session_key is missing, except for the auth URL itself
            if self.session_key is None and method != "POST" and url != API_AUTH_URL:
                _LOGGER.warning(
                    "No session key found. Attempting to authenticate.")
                await self.auth()

            # check if the session key is valid
            await self.ensure_valid_session()

            # Prepare the data for the API request
            kwargs = self.prepare_data(kwargs)

            # Send the request and wait for the response
            async with self.session.request(method, url, **kwargs) as response:
                response.raise_for_status()
                parsed_response = await response.json()

                # Handle specific status code 40302
                if parsed_response.get("status_code", 0) == 40302:
                    _LOGGER.warning(
                        "Received 40302 status code. Attempting to re-authenticate.")

                return parsed_response

        except (aiohttp.ClientResponseError, aiohttp.ClientConnectionError) as e:
            _LOGGER.error(f"Client error occurred in _request: {e}")
            raise APIError(f"API request failed {method} {url}") from e
        except Exception as e:
            _LOGGER.error(f"Unexpected error occurred in _request: {e}")
            raise APIError(f"API request failed {method} {url}") from e

    @staticmethod
    def encrypt_password(public_key_str, password):
        try:
            rsa_key = RSA.importKey(public_key_str)
            cipher = PKCS1_v1_5.new(rsa_key)
            return b64encode(cipher.encrypt(bytes(password, "utf-8")))
        except Exception as e:
            _LOGGER.error(f"Encryption error occurred in encrypt_password: {e}")
            raise

    async def auth(self):
        if not self.email or not self.password:
            await self.close()
            raise AuthenticationError("Email and password must be provided")

        # Check if public_key is None
        if self.public_key is None:
            _LOGGER.error("Public key is None.")
            await self.close()
            raise AuthenticationError("Public key is None.")

        try:
            encrypted_password = self.encrypt_password(self.public_key, self.password)
        except Exception as e:
            _LOGGER.error(f"An error occurred while encrypting the password: {e}")
            await self.close()
            return

        data = {"secure_flag": "1", "email": self.email,
                "password": encrypted_password}
        parsed = await self._request("POST", API_AUTH_URL, json=data)

        # Check if parsed object is None
        if parsed is None:
            _LOGGER.error("Parsed object is None.")
            await self.close()
            raise AuthenticationError("Received NoneType object.")

        # Check for 'terminal_user_session_key'
        if "terminal_user_session_key" not in parsed:
            _LOGGER.error(
                "'terminal_user_session_key' not found in parsed object.")
            await self.close()
            raise AuthenticationError("'terminal_user_session_key' missing.")

        # If everything is fine, set the session_key
        self.session_key = parsed["terminal_user_session_key"]
        self.session_key_expiry = datetime.datetime.now() + datetime.timedelta(minutes=10)
        return parsed

    async def ensure_valid_session(self):
        """Ensure the session is valid and authenticated."""
        if not self.is_session_valid():
            _LOGGER.warning("Session key expired or missing. Re-authenticating.")
            await self.auth()

    def is_session_valid(self):
        """Check if the session key is valid."""
        return True

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
            _LOGGER.error(f"Aiohttp client error in get_scale_users: {e}")
        except Exception as e:
            _LOGGER.error(f"An unexpected error occurred in get_scale_users: {e}")
        return None

    async def get_measurements(self) -> Optional[List[Dict]]:
        """
        Asynchronously fetches the most recent weight measurements for the user.

        Returns:
            Optional[List[Dict]]: A list of dictionaries containing the most recent weight measurements for the user.
                                Returns None if the request fails or if 'last_ary' is not present in the response.

        Raises:
            aiohttp.ClientError: For client-related errors.
            Exception: For any other unexpected errors.
        """
        try:
            ago_timestamp = int(time.mktime(datetime.date(1998, 1, 1).timetuple()))
            url = f"{API_MEASUREMENTS_URL}?user_id={self.user_id}&last_at={ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
            parsed = await self._request("GET", url)

            if not parsed:
                _LOGGER.error(f"Invalid response {url}")
                await self.close()
                return None

            if "last_ary" not in parsed:
                _LOGGER.warning(f"Invalid response or 'last_ary' not in the response. {url}")
                await self.close()
                return None

            last_measurement = parsed['last_ary'][0] if parsed['last_ary'] else None

            if last_measurement and isinstance(last_measurement, dict):
                self.weight = last_measurement.get("weight", None)
                self.time_stamp = last_measurement.get("time_stamp", None)
            else:
                _LOGGER.warning("Invalid last_measurement value.")
                self.weight = None
                self.time_stamp = None

            return parsed["last_ary"]

        except aiohttp.ClientError as e:
            _LOGGER.error(f"Aiohttp client error: {e} {url}")
            await self.close()
            return None
        except Exception as e:
            _LOGGER.error(f"An unexpected error occurred in get_measurements: {e} {url}")
            await self.close()
            return None

    async def get_weight(self):
        last_measurement = await self.get_measurements()
        return self.weight, last_measurement[0] if last_measurement else None

    async def get_specific_metric(
        self, metric_type: str, metric: str, user_id: Optional[str] = None
    ) -> Optional[float]:
        """
        Fetch a specific metric for a particular user ID based on the type specified.

        Parameters:
            metric_type (str): The type of metric to fetch.
            metric (str): The specific metric to fetch.
            user_id (Optional[str]): The user ID for whom to fetch the metric. Defaults to None.

        Returns:
            Optional[float]: The fetched metric value, or None if it couldn't be fetched.
        """

        METRIC_TYPE_FUNCTIONS = {
            METRIC_TYPE_GIRTH: ("list_girth", "girths"),
            METRIC_TYPE_GIRTH_GOAL: ("list_girth_goal", "girth_goals"),
            METRIC_TYPE_GROWTH_RECORD: ("list_growth_record", "growths"),
        }

        if user_id:
            self.set_user_id(user_id)

        if metric_type == METRIC_TYPE_WEIGHT:
            last_measurement = await self.get_weight()
            if last_measurement and self.weight is not None:
                return last_measurement[1].get(metric, None) if last_measurement[1] else None
        try:
            if metric_type == METRIC_TYPE_GIRTH_GOAL:
                return await self.get_specific_girth_goal_metric(metric, user_id)

            func_name, last_measurement_key = METRIC_TYPE_FUNCTIONS.get(metric_type, ("weight", None))

            if func_name is None:
                _LOGGER.error(f"Invalid metric_type: {metric_type}. Must be one of {list(METRIC_TYPE_FUNCTIONS.keys())}.")
                await self.close()
                return None

            func: Callable = getattr(self, func_name)
            metric_info = await func()

            if metric_info is None or last_measurement_key not in metric_info:
                await self.close()
                return None

            last_measurement = metric_info[last_measurement_key][0] if metric_info[last_measurement_key] else None

            if last_measurement is None:
                _LOGGER.warning(f"Invalid response or '{last_measurement_key}' not in the response.")
                await self.close()
                return None

            return last_measurement.get(metric, None) if last_measurement else None

        except Exception as e:
            _LOGGER.error(f"An error occurred in get_specific_metric: {e} {metric_type} {metric}")
            await self.close()
            return None

    async def get_info(self):
        """
        Wrapper method to authenticate, fetch users, and get measurements.
        """
        await self.auth()
        await self.get_scale_users()
        return await self.get_measurements()

    async def start_polling(self, refresh=0):
        """
        Start polling for weight data at a given interval.
        """
        if refresh <= 0:
            refresh = self.refresh
        self.is_polling_active = True
        refresh = refresh if refresh > 0 else 60  # Update local variable
        try:
            await self.get_info()
            while True:
                await asyncio.sleep(refresh)  # Use local variable
                await self.get_info()
        except Exception as e:
            _LOGGER.error(f"An exception occurred during polling: {e}")
            self.stop_polling()  # Stop polling
        finally:
            await self.close()  # Close session

    def stop_polling(self):
        """
        Stop polling for weight data.
        """
        if not self.is_polling_active:
            return
        if hasattr(self, "polling"):
            try:
                # Check if 'polling' is a Timer object or similar with a 'cancel' method
                if callable(getattr(self.polling, "cancel", None)):
                    self.polling.cancel()
                    _LOGGER.info("Successfully stopped polling.")
                    self.is_polling_active = False
                else:
                    _LOGGER.warning(
                        "Attribute 'polling' exists but has no 'cancel' method.")
            except Exception as e:
                _LOGGER.error(
                    f"An error occurred while stopping polling: {e}")
        else:
            _LOGGER.warning("No active polling to stop.")

    async def get_device_info(self):
        """
        Asynchronously get device information.
        Returns:
            dict: The API response as a dictionary.
        """
        week_ago_timestamp = self.get_ago_timestamp()
        url = f"{DEVICE_INFO_URL}?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            return await self._request("GET", url)
        except Exception as e:
            _LOGGER.error(f"An error occurred while listing device info: {e}")
            return None

    async def list_latest_model(self):
        """
        Asynchronously list the latest model information.

        Returns:
            dict: The API response as a dictionary.
        """
        week_ago_timestamp = self.get_ago_timestamp()
        url = f"{LATEST_MODEL_URL}?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            return await self._request("GET", url)
        except Exception as e:
            _LOGGER.error(f"An error occurred while listing latest model: {e}")
            return None

    async def list_girth(self) -> Optional[dict]:
        """
        Asynchronously list girth information.

        Returns:
            Optional[dict]: The API response as a dictionary, or None if the request fails.
        """
        week_ago_timestamp = self.get_ago_timestamp()
        url = f"{GIRTH_URL}?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            return await self._request("GET", url)
        except Exception as e:
            _LOGGER.error(f"An error occurred while listing girth: {e}")
            return None

    async def get_specific_girth_metric(
        self, metric: str, user_id: Optional[str] = None
    ) -> Optional[float]:
        """
        Fetch a specific girth metric for a particular user ID based on the most recent girth information.

        Parameters:
            metric (str): The specific metric to fetch (e.g., "waist", "hip").
            user_id (Optional[str]): The user ID for whom to fetch the metric. Defaults to None.

        Returns:
            Optional[float]: The fetched metric value, or None if it couldn't be fetched.
        """
        try:
            if user_id:
                self.set_user_id(user_id)
            girth_info = await self.list_girth()
            last_measurement = (
                girth_info.get("girths", [])[0]
                if girth_info.get("girths")
                else None
            )
            return last_measurement.get(metric, None) if last_measurement else None
        except Exception as e:
            _LOGGER.error(f"An error occurred in get_specific_girth_metric: {e}")
            return None

    async def list_girth_goal(self):
        """
        Asynchronously list girth goal information.

        Returns:
            dict: The API response as a dictionary.
        """
        week_ago_timestamp = self.get_ago_timestamp()
        url = f"{GIRTH_GOAL_URL}?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            return await self._request("GET", url)
        except Exception as e:
            _LOGGER.error(f"An error occurred while listing girth goal: {e}")
            return None

    async def get_specific_girth_goal_metric(
        self, metric: str, user_id: Optional[str] = None
    ) -> Optional[float]:
        """
        Fetch a specific girth goal metric for a particular user ID from the most recent girth goal information.

        Parameters:
            metric (str): The specific metric to fetch.
            user_id (str, optional): The user ID for whom to fetch the metric. Defaults to None.

        Returns:
            float, None: The fetched metric value, or None if it couldn't be fetched.
        """
        try:
            if user_id:
                self.set_user_id(user_id)

            girth_goal_info = await self.list_girth_goal()

            if not girth_goal_info or 'girth_goals' not in girth_goal_info:
                return None

            if last_goal := next(
                (
                    goal
                    for goal in girth_goal_info['girth_goals']
                    if goal['girth_type'] == metric
                ),
                None,
            ):
                return last_goal.get('goal_value', None)

            return None

        except Exception as e:
            await self.close()
            print(f"An error occurred in get_specific_girth_goal_metric: {e}")
            return None

    async def list_growth_record(self):
        """
        Asynchronously list growth records.
        Returns:
            dict: The API response as a dictionary.
        """
        week_ago_timestamp = self.get_ago_timestamp()
        url = f"{GROWTH_RECORD_URL}?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            return await self._request("GET", url)
        except Exception as e:
            await self.close()
            print(f"An error occurred in list_growth_record: {e}")
            return None

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
            growth_info = await self.list_growth_record()
            last_measurement = (
                growth_info.get("growths", [])[0]
                if growth_info.get("growths")
                else None
            )
            return last_measurement.get(metric, None) if last_measurement else None
        except Exception as e:
            await self.close()
            print(f"An error occurred in get_specific_growth_metric: {e}")
            return None

    async def message_list(self):
        """
        Asynchronously list messages.
        """
        week_ago_timestamp = self.get_ago_timestamp()
        url = f"{MESSAGE_LIST_URL}?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            return await self._request("GET", url)
        except Exception as e:
            await self.close()
            print(f"An error occurred in message_list: {e}")
            return None

    async def request_user(self):
        """
        Asynchronously request user
        """
        week_ago_timestamp = self.get_ago_timestamp()
        url = f"{USER_REQUEST_URL}?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            return await self._request("GET", url)
        except Exception as e:
            await self.close()
            print(f"An error occurred in request_user: {e}")
            return None

    async def reach_goal(self):
        """
        Asynchronously reach_goal
        """
        week_ago_timestamp = self.get_ago_timestamp()
        url = f"{USERS_REACH_GOAL}?user_id={self.user_id}&last_updated_at={week_ago_timestamp}&locale=en&app_id=Renpho&terminal_user_session_key={self.session_key}"
        try:
            return await self._request("GET", url)
        except Exception as e:
            await self.close()
            print(f"An error occurred in reach_goal: {e}")
            return None

    async def close(self):
        """
        Shutdown the executor when you are done using the RenphoWeight instance.
        """
        self.stop_polling()  # Stop the polling
        if self.session and not self.session.closed:
            self.session_key = None
            self.session_key_expiry = datetime.datetime.now()
            await self.session.close()  # Close the session


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


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    try:
        return RenphoWeight(credentials.username, credentials.password)
    except Exception as e:
        # Log the error here if you want
        raise HTTPException(
            status_code=401, detail="MarketWatch validation failed"
        ) from e


@app.get("/")
def read_root(request: Request):
    return "Renpho API"

@app.get("/auth")
async def auth(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        await renpho.auth()
        return {"status": "success", "message": "Authentication successful."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/info")
async def get_info(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        await renpho.get_info()
        return {"status": "success", "message": "Fetched user info."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/users")
async def get_scale_users(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        users = await renpho.get_scale_users()
        return {"status": "success", "message": "Fetched scale users.", "data": users}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/measurements")
async def get_measurements(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        measurements = await renpho.get_measurements()
        return {"status": "success", "message": "Fetched measurements.", "data": measurements}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/weight")
async def get_weight(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        weight = await renpho.get_weight()
        return {"status": "success", "message": "Fetched weight.", "data": weight[0]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/specific_metric")
async def get_specific_metric(request: Request, metric: str, metric_id: str, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        specific_metric = await renpho.get_specific_metric(metric, metric_id)
        return {"status": "success", "message": f"Fetched specific metric: {specific_metric}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/device_info")
async def get_device_info(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        device_info = await renpho.get_device_info()
        return {"status": "success", "message": "Fetched device info.", "data": device_info}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/latest_model")
async def list_latest_model(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        latest_model = await renpho.list_latest_model()
        return {"status": "success", "message": "Fetched latest model.", "data": latest_model}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/girth_info")
async def list_girth(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        girth_info = await renpho.list_girth()
        return {"status": "success", "message": "Fetched girth info.", "data": girth_info}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/girth_goal")
async def list_girth_goal(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        girth_goal = await renpho.list_girth_goal()
        return {"status": "success", "message": "Fetched girth goal.", "data": girth_goal}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/growth_record")
async def list_growth_record(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        growth_record = await renpho.list_growth_record()
        return {"status": "success", "message": "Fetched growth record.", "data": growth_record}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/message_list")
async def message_list(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        messages = await renpho.message_list()
        return {"status": "success", "message": "Fetched message list.", "data": messages}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/reach_goal")
async def reach_goal(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        reach_goal = await renpho.reach_goal()
        return {"status": "success", "message": "Fetched reach_goal.", "data": reach_goal}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/request_user")
async def request_user(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        request_user = await renpho.request_user()
        return {"status": "success", "message": "Fetched request user.", "data": request_user}
    except Exception as e:
        return {"status": "error", "message": str(e)}
