import unittest
from unittest.mock import Mock, patch
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64decode, b64encode

import requests
from sensor import RenphoSensor, WeightSensor, TimeSensor, setup_platform
from RenphoWeight import RenphoWeight
from __init__ import setup


class TestEncryption(unittest.TestCase):
    """Test cases for the encryption logic"""

    def setUp(self):
        """Initial setup for test cases."""
        # Public key for testing encryption
        self.public_key = '''-----BEGIN PUBLIC KEY-----
                            MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+25I2upukpfQ7rIaaTZtVE744
                            u2zV+HaagrUhDOTq8fMVf9yFQvEZh2/HKxFudUxP0dXUa8F6X4XmWumHdQnum3zm
                            Jr04fz2b2WCcN0ta/rbF2nYAnMVAk2OJVZAMudOiMWhcxV1nNJiKgTNNr13de0EQ
                            IiOL2CUBzu+HmIfUbQIDAQAB
                            -----END PUBLIC KEY-----'''
        self.key = RSA.importKey(self.public_key)
        self.cipher = PKCS1_v1_5.new(self.key)

    def test_encryption(self):
        """Test the encryption logic."""
        test_password = "my_password"
        encrypted_password = b64encode(
            self.cipher.encrypt(bytes(test_password, 'utf-8')))

        # For now, just check if encryption doesn't return the original password
        self.assertNotEqual(test_password, encrypted_password.decode('utf-8'))

class TestRenphoWeight(unittest.TestCase):
    """Test cases for the RenphoWeight class"""

    def setUp(self):
        """Initial setup for test cases."""
        self.mock_response = Mock()
        self.renpho = RenphoWeight('public_key', 'test@email.com', 'password')

    @patch('requests.post')
    def test_auth(self, mock_post):
        """Test the authentication logic."""
        self.mock_response.json.return_value = {
            'terminal_user_session_key': 'session_key'}
        mock_post.return_value = self.mock_response

        result = self.renpho.auth()

        self.assertEqual(result, {'terminal_user_session_key': 'session_key'})
        self.assertEqual(self.renpho.session_key, 'session_key')

    @patch('requests.get')
    def test_getScaleUsers(self, mock_get):
        """Test fetching the scale users."""
        self.mock_response.json.return_value = {
            'scale_users': [{'user_id': '1'}]}
        mock_get.return_value = self.mock_response

        result = self.renpho.getScaleUsers()

        self.assertEqual(result, [{'user_id': '1'}])
        self.assertEqual(self.renpho.user_id, '1')

    @patch('requests.get')
    def test_getMeasurements(self, mock_get):
        """Test fetching the measurements."""
        self.mock_response.json.return_value = {
            'last_ary': [{'weight': 70, 'time_stamp': 1630886400}]}
        mock_get.return_value = self.mock_response

        result = self.renpho.getMeasurements()

        self.assertEqual(result, [{'weight': 70, 'time_stamp': 1630886400}])
        self.assertEqual(self.renpho.weight, 70)
        self.assertEqual(self.renpho.time_stamp, 1630886400)

    @patch('requests.post')
    @patch('requests.get')
    def test_getInfo(self, mock_get, mock_post):
        """Test the wrapper method getInfo."""
        self.mock_response.json.side_effect = [
            {'terminal_user_session_key': 'session_key'},
            {'scale_users': [{'user_id': '1'}]},
            {'last_ary': [{'weight': 70, 'time_stamp': 1630886400}]}
        ]
        mock_get.return_value = self.mock_response
        mock_post.return_value = self.mock_response

        self.renpho.getInfo()

        self.assertEqual(self.renpho.session_key, 'session_key')
        self.assertEqual(self.renpho.user_id, '1')
        self.assertEqual(self.renpho.weight, 70)
        self.assertEqual(self.renpho.time_stamp, 1630886400)

    @patch('requests.post')
    def test_failed_auth(self, mock_post):
        """Test failed authentication logic."""
        self.mock_response.json.return_value = {'error': 'Invalid credentials'}
        mock_post.return_value = self.mock_response

        result = self.renpho.auth()

        self.assertIsNone(result)
        self.assertIsNone(self.renpho.session_key)

    @patch('requests.get')
    def test_no_scale_users(self, mock_get):
        """Test no scale users are returned."""
        self.mock_response.json.return_value = {'scale_users': []}
        mock_get.return_value = self.mock_response

        result = self.renpho.getScaleUsers()

        self.assertEqual(result, [])
        self.assertIsNone(self.renpho.user_id)

    @patch('requests.get')
    def test_no_measurements(self, mock_get):
        """Test no measurements are returned."""
        self.mock_response.json.return_value = {'last_ary': []}
        mock_get.return_value = self.mock_response

        result = self.renpho.getMeasurements()

        self.assertEqual(result, [])
        self.assertIsNone(self.renpho.weight)
        self.assertIsNone(self.renpho.time_stamp)

    @patch('requests.get')
    def test_get_specific_metric_not_found(self, mock_get):
        """Test fetching a specific metric that does not exist."""
        mock_response = Mock()
        mock_response.json.return_value = {'last_ary': [{'weight': 70, 'time_stamp': 1630886400}]}
        mock_get.return_value = mock_response

        metric_value = self.renpho.getSpecificMetric("unknown_metric")

        self.assertIsNone(metric_value)

    def test_get_specific_metric_no_measurements(self):
        """Test fetching a specific metric with no prior measurements."""
        self.renpho.time_stamp = None  # Simulating no prior measurements

        metric_value = self.renpho.getSpecificMetric("bodyfat")

        self.assertIsNone(metric_value)

    @patch('requests.get')
    def test_get_info_fail(self, mock_get):
        """Test getInfo method failure."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("Info fetch failed")
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            self.renpho.getInfo()

class TestRenphoSensor(unittest.TestCase):

    def setUp(self):
        self.renpho = Mock()
        self.renpho.getSpecificMetric.return_value = 75  # kg
        self.sensor = RenphoSensor(self.renpho, "weight", "Weight", "kg")

    def test_name(self):
        """Test name property."""
        self.assertEqual(self.sensor.name, "Renpho Weight")

    def test_state(self):
        """Test state property."""
        self.sensor.update()
        self.assertEqual(self.sensor.state, 75)

    def test_unit_of_measurement(self):
        """Test unit_of_measurement property."""
        self.assertEqual(self.sensor.unit_of_measurement, "kg")

    def test_category(self):
        """Test category property."""
        self.assertEqual(self.sensor.category, "Renpho")

    def test_label(self):
        """Test label property."""
        self.assertEqual(self.sensor.label, "Data")

    def test_update_fail(self):
        """Test update method failure."""
        self.renpho.getSpecificMetric.side_effect = Exception("API Error")
        with self.assertRaises(Exception):
            self.sensor.update()

class TestSetupPlatform(unittest.TestCase):

    def setUp(self):
        self.hass = Mock()
        self.config = {}
        self.add_entities = Mock()

    @patch('sensor.RenphoSensor')
    def test_setup_platform(self, MockRenphoSensor):
        renpho = Mock()
        self.hass.data = {'renpho': renpho}

        setup_platform(self.hass, self.config, self.add_entities)

        self.add_entities.assert_called_once()  # Check if entities were added



class TestSetup(unittest.TestCase):
    """Test cases for the setup function of the Renpho component."""

    def setUp(self):
        """Initial setup for test cases."""
        self.hass = Mock()  # Mocked Home Assistant core object
        self.config = {
            DOMAIN: {
                CONF_EMAIL: 'test@email.com',  # Mock email
                CONF_PASSWORD: 'password',     # Mock password
                CONF_REFRESH: 60               # Mock refresh rate
            }
        }
        self.renpho = Mock()  # Mocked RenphoWeight object

    # Replace with the actual import path
    @patch('your_init_module.RenphoWeight')
    def test_setup(self, MockRenphoWeight):
        """Test the setup function."""
        # Mock the return value of RenphoWeight instantiation
        MockRenphoWeight.return_value = self.renpho

        # Call the setup function with the mocked Home Assistant and configuration
        result = setup(self.hass, self.config)

        # Check if setup was successful
        self.assertTrue(result)

        # Check if EVENT_HOMEASSISTANT_START event is registered
        self.hass.bus.listen_once.assert_called_with(
            EVENT_HOMEASSISTANT_START, any)  # Replace `any` with the actual function

        # Check if RenphoWeight object is stored in Home Assistant's data dictionary
        self.assertEqual(self.hass.data[DOMAIN], self.renpho)


if __name__ == "__main__":
    unittest.main()
