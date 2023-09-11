# Renpho Weight Scale Integration for Home Assistant

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> This project is inspired by the original Renpho integration. Check it out [here](https://github.com/neilzilla/hass-renpho/tree/master)
> Download the [Renpho Android App](https://play.google.com/store/apps/details?id=com.qingniu.renpho&hl=en&gl=US).

## Overview

This custom component allows you to integrate Renpho's weight scale data into Home Assistant. It fetches weight and various other health metrics and displays them as sensors in Home Assistant.

## Table of Contents

- [Prerequisites](#prerequisites)
- [File Structure](#file-structure)
- [Supported Metrics](#supported-metrics)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [API endpoints](#api-endpoints)

## Prerequisites

1. You must have a Renpho account. If you don't have one, you can create one [here](https://renpho.com/).
2. You must have a Renpho scale. If you don't have one, you can purchase one [here](https://renpho.com/collections/body-fat-scale).
3. You must have the Renpho app installed on your mobile device. You can download it [here](https://play.google.com/store/apps/details?id=com.renpho.smart&hl=en_US&gl=US) for Android and [here](https://apps.apple.com/us/app/renpho/id1115563582) for iOS.
4. You must have Home Assistant installed and running.
5. You must have the [Home Assistant Community Store (HACS)](https://hacs.xyz/) installed and running.
6. Visual Studio Code is recommended for editing the files.

## File Structure

The following shows the organization of the project's files and directories:

```
.
├── .gitignore                # To ignore files that should not be committed
├── README.md                 # Project overview and setup guide
├── SECURITY.md               # Security policy
├── __init__.py               # Main file to initialize the component
├── docs
│   └── README.md             # Detailed documentation
├── example
│   ├── configuration.yaml    # Example Home Assistant configuration
│   └── lovelace.yaml         # Example Lovelace UI configuration
├── manifest.json             # Information about the component
├── requirements.txt          # List of Python packages required
└── src
    ├── RenphoWeight.py       # Core logic for the Renpho weight scale
    ├── __init__.py           # Initialization within src folder
    ├── const.py              # Constants used in the component
    ├── sensor.py             # Sensor-related code
    └── tests.py              # Unit tests
```

## Supported Metrics

### General Information

| Metric        | Description                                  | Data Type | Unit of Measurement |
| ------------- | -------------------------------------------- | --------- | ------------------- |
| id            | Unique identifier for the record             | Numeric   | N/A                 |
| b_user_id     | Unique identifier for the user               | Numeric   | N/A                 |
| time_stamp    | Unix timestamp for the record                | Numeric   | UNIX Time           |
| created_at    | Time the data was created                    | DateTime  | N/A                 |
| created_stamp | Unix timestamp for when the data was created | Numeric   | UNIX Time           |

### Device Information

| Metric         | Description               | Data Type | Unit of Measurement |
| -------------- | ------------------------- | --------- | ------------------- |
| scale_type     | Type of scale used        | Numeric   | N/A                 |
| scale_name     | Name of the scale         | String    | N/A                 |
| mac            | MAC address of the device | String    | N/A                 |
| internal_model | Internal model code       | String    | N/A                 |
| time_zone      | Time zone information     | String    | N/A                 |

### User Profile

| Metric      | Description            | Data Type | Unit of Measurement |
| ----------- | ---------------------- | --------- | ------------------- |
| gender      | Gender of the user     | Numeric   | N/A                 |
| height      | Height of the user     | Numeric   | cm                  |
| height_unit | Unit for height        | Numeric   | N/A                 |
| birthday    | Birth date of the user | Date      | N/A                 |

### Physical Metrics

| Metric    | Description         | Data Type | Unit of Measurement |
| --------- | ------------------- | --------- | ------------------- |
| weight    | Body weight         | Numeric   | kg                  |
| bmi       | Body Mass Index     | Numeric   | N/A                 |
| muscle    | Muscle mass         | Numeric   | %                   |
| bone      | Bone mass           | Numeric   | %                   |
| waistline | Waistline size      | Numeric   | cm                  |
| hip       | Hip size            | Numeric   | cm                  |
| stature   | Stature information | Numeric   | cm                  |

### Body Composition

| Metric  | Description               | Data Type | Unit of Measurement |
| ------- | ------------------------- | --------- | ------------------- |
| bodyfat | Body fat percentage       | Numeric   | %                   |
| water   | Water content in the body | Numeric   | %                   |
| subfat  | Subcutaneous fat          | Numeric   | %                   |
| visfat  | Visceral fat level        | Numeric   | Level               |

### Metabolic Metrics

| Metric  | Description                 | Data Type | Unit of Measurement |
| ------- | --------------------------- | --------- | ------------------- |
| bmr     | Basal Metabolic Rate        | Numeric   | kcal/day            |
| protein | Protein content in the body | Numeric   | %                   |

### Age Metrics

| Metric  | Description              | Data Type | Unit of Measurement |
| ------- | ------------------------ | --------- | ------------------- |
| bodyage | Estimated biological age | Numeric   | Years               |

Certainly, you can expand the existing table to include the "Unit of Measurement" column for each metric. Here's how you can continue to organize the metrics into categories, similar to your previous table, but now with the added units:

### Electrical Measurements (not sure if this is the correct name)

| Metric                  | Description                            | Data Type | Unit of Measurement |
| ----------------------- | -------------------------------------- | --------- | ------------------- |
| resistance              | Electrical resistance                  | Numeric   | Ohms                |
| sec_resistance          | Secondary electrical resistance        | Numeric   | Ohms                |
| actual_resistance       | Actual electrical resistance           | Numeric   | Ohms                |
| actual_sec_resistance   | Actual secondary electrical resistance | Numeric   | Ohms                |
| resistance20_left_arm   | Resistance20 in the left arm           | Numeric   | Ohms                |
| resistance20_left_leg   | Resistance20 in the left leg           | Numeric   | Ohms                |
| resistance20_right_leg  | Resistance20 in the right leg          | Numeric   | Ohms                |
| resistance20_right_arm  | Resistance20 in the right arm          | Numeric   | Ohms                |
| resistance20_trunk      | Resistance20 in the trunk              | Numeric   | Ohms                |
| resistance100_left_arm  | Resistance100 in the left arm          | Numeric   | Ohms                |
| resistance100_left_leg  | Resistance100 in the left leg          | Numeric   | Ohms                |
| resistance100_right_arm | Resistance100 in the right arm         | Numeric   | Ohms                |
| resistance100_right_leg | Resistance100 in the right leg         | Numeric   | Ohms                |
| resistance100_trunk     | Resistance100 in the trunk             | Numeric   | Ohms                |

### Cardiovascular Metrics

| Metric        | Description   | Data Type | Unit of Measurement |
| ------------- | ------------- | --------- | ------------------- |
| heart_rate    | Heart rate    | Numeric   | bpm                 |
| cardiac_index | Cardiac index | Numeric   | N/A                 |

### Other Metrics

| Metric           | Description                          | Data Type | Unit of Measurement |
| ---------------- | ------------------------------------ | --------- | ------------------- |
| method           | Method used for measurement          | Numeric   | N/A                 |
| sport_flag       | Sports flag                          | Numeric   | N/A                 |
| left_weight      | Weight on the left side of the body  | Numeric   | kg                  |
| right_weight     | Weight on the right side of the body | Numeric   | kg                  |
| waistline        | Waistline size                       | Numeric   | cm                  |
| hip              | Hip size                             | Numeric   | cm                  |
| local_created_at | Local time the data was created      | DateTime  | N/A                 |
| time_zone        | Time zone information                | String    | N/A                 |
| remark           | Additional remarks                   | String    | N/A                 |
| score            | Health score                         | Numeric   | N/A                 |
| pregnant_flag    | Pregnancy flag                       | Numeric   | N/A                 |
| stature          | Stature information                  | Numeric   | cm                  |
| category         | Category identifier                  | Numeric   | N/A                 |

### Girth Measurements

| Metric            | Description       | Data Type | Unit of Measurement | Category     | Label              |
| ----------------- | ----------------- | --------- | ------------------- | ------------ | ------------------ |
| neck_value        | Neck Value        | Numeric   | cm                  | Measurements | Girth Measurements |
| shoulder_value    | Shoulder Value    | Numeric   | cm                  | Measurements | Girth Measurements |
| arm_value         | Arm Value         | Numeric   | cm                  | Measurements | Girth Measurements |
| chest_value       | Chest Value       | Numeric   | cm                  | Measurements | Girth Measurements |
| waist_value       | Waist Value       | Numeric   | cm                  | Measurements | Girth Measurements |
| hip_value         | Hip Value         | Numeric   | cm                  | Measurements | Girth Measurements |
| thigh_value       | Thigh Value       | Numeric   | cm                  | Measurements | Girth Measurements |
| calf_value        | Calf Value        | Numeric   | cm                  | Measurements | Girth Measurements |
| left_arm_value    | Left Arm Value    | Numeric   | cm                  | Measurements | Girth Measurements |
| left_thigh_value  | Left Thigh Value  | Numeric   | cm                  | Measurements | Girth Measurements |
| left_calf_value   | Left Calf Value   | Numeric   | cm                  | Measurements | Girth Measurements |
| right_arm_value   | Right Arm Value   | Numeric   | cm                  | Measurements | Girth Measurements |
| right_thigh_value | Right Thigh Value | Numeric   | cm                  | Measurements | Girth Measurements |
| right_calf_value  | Right Calf Value  | Numeric   | cm                  | Measurements | Girth Measurements |
| whr_value         | WHR Value         | Numeric   | ratio               | Measurements | Girth Measurements |
| abdomen_value     | Abdomen Value     | Numeric   | cm                  | Measurements | Girth Measurements |

---

### Girth Goals

| Metric                 | Description            | Data Type | Unit of Measurement | Category | Label       |
| ---------------------- | ---------------------- | --------- | ------------------- | -------- | ----------- |
| neck_goal_value        | Neck Goal Value        | Numeric   | cm                  | Goals    | Girth Goals |
| shoulder_goal_value    | Shoulder Goal Value    | Numeric   | cm                  | Goals    | Girth Goals |
| arm_goal_value         | Arm Goal Value         | Numeric   | cm                  | Goals    | Girth Goals |
| chest_goal_value       | Chest Goal Value       | Numeric   | cm                  | Goals    | Girth Goals |
| waist_goal_value       | Waist Goal Value       | Numeric   | cm                  | Goals    | Girth Goals |
| hip_goal_value         | Hip Goal Value         | Numeric   | cm                  | Goals    | Girth Goals |
| thigh_goal_value       | Thigh Goal Value       | Numeric   | cm                  | Goals    | Girth Goals |
| calf_goal_value        | Calf Goal Value        | Numeric   | cm                  | Goals    | Girth Goals |
| left_arm_goal_value    | Left Arm Goal Value    | Numeric   | cm                  | Goals    | Girth Goals |
| left_thigh_goal_value  | Left Thigh Goal Value  | Numeric   | cm                  | Goals    | Girth Goals |
| left_calf_goal_value   | Left Calf Goal Value   | Numeric   | cm                  | Goals    | Girth Goals |
| right_arm_goal_value   | Right Arm Goal Value   | Numeric   | cm                  | Goals    | Girth Goals |
| right_thigh_goal_value | Right Thigh Goal Value | Numeric   | cm                  | Goals    | Girth Goals |
| right_calf_goal_value  | Right Calf Goal Value  | Numeric   | cm                  | Goals    | Girth Goals |
| whr_goal_value         | WHR Goal Value         | Numeric   | ratio               | Goals    | Girth Goals |
| abdomen_goal_value     | Abdomen Goal Value     | Numeric   | cm                  | Goals    | Girth Goals |

## Installation

1. Copy this folder to `<config_dir>/custom_components/hass_renpho/`.
2. Add the necessary configuration to your `configuration.yaml` file.

## Configuration

Add the following entry in your `configuration.yaml`:

```yaml
renpho:
  email: your_email@example.com # email address
  password: YourSecurePassword # password
  refresh: 600 # time to poll (ms)
  user_id: 123456789 # user ID (optional)
```

Then add the sensor platform:

```yaml
sensor:
  platform: renpho
```

## API Documentation

The `RenphoWeight` class is the core of this integration, providing methods to interact with the Renpho API. Below are detailed explanations of the methods available in this class.

### `auth()`

#### Description

Authenticates the user with the Renpho API and fetches a session key. The session key is stored within the class and is used for subsequent API calls.

#### Parameters

None

#### Returns

- `dict`: Parsed JSON response from the API containing the session key and other authentication details.

### `get_scale_users()`

#### Description

Fetches the list of users associated with the Renpho scale.

#### Parameters

None

#### Returns

- `list`: A list of dictionaries, each containing details of a user (e.g., user ID, name).

### `get_measurements()`

#### Description

Retrieves the latest weight measurements for the user specified by `user_id`. This method updates the `weight` and `time_stamp` attributes of the class.

#### Parameters

None

#### Returns

- `list`: A list of dictionaries containing the latest measurements.

### `get_specific_metric(metric)`

#### Description

Retrieves a specific metric from the most recent weight measurement.

#### Parameters

- `metric (str)`: The specific metric to retrieve (e.g., 'weight', 'bmi').

#### Returns

- `float`: The value of the specified metric.
- `None`: If the metric is not found.

### `get_specific_metric_from_user_ID(metric, user_id=None)`

#### Description

Retrieves a specific metric for a particular user ID from the most recent weight measurement.

#### Parameters

- `metric (str)`: The metric to fetch (e.g., 'bodyfat', 'water').
- `user_id (str, optional)`: The user ID for whom the metric should be fetched. Defaults to the object's `user_id` if not provided.

#### Returns

- `float`: Value of the specified metric.
- `None`: If an error occurs or the metric is not found.

### `start_polling(polling_interval=60)`

#### Description

Starts polling for weight data at a given interval. The polling will automatically call `get_measurements()` at the specified interval.

#### Parameters

- `polling_interval (int)`: Time in seconds between each polling call. Defaults to 60 seconds.

#### Returns

None

### `stop_polling()`

#### Description

Stops the ongoing polling for weight data.

#### Parameters

None

#### Returns

None

## API endpoints

This document describes the API endpoints and methods utilized by the `RenphoWeight` class in the Home Assistant custom component for Renpho weight scales. It outlines the endpoints, expected parameters, and returned data.

---

## Authentication

### API_AUTH_URL

#### Endpoint

`https://renpho.qnclouds.com/api/v3/users/sign_in.json?app_id=Renpho`

#### HTTP Method

`POST`

#### Parameters

- `app_id`: Application identifier (fixed as "Renpho").
- `email`: User's email address for Renpho account.
- `password`: Encrypted password for the Renpho account.

#### Returns

JSON payload containing:

- `session_key`: Session key for future API calls.

#### Usage in Code

This URL is used in the `auth()` method to authenticate the user and fetch the session key.

---

## User Information

### API_SCALE_USERS_URL

#### Endpoint

`https://renpho.qnclouds.com/api/v3/scale_users/list_scale_user`

#### HTTP Method

`GET`

#### Parameters

- `locale`: Language/locale setting, usually "en".
- `terminal_user_session_key`: Session key obtained from authentication.

#### Returns

JSON payload containing:

- `users`: Array of user objects containing user details like user ID, scale user ID, MAC address, and more.

#### Usage in Code

This URL is used in the `get_scale_users()` method to fetch the list of users associated with the scale.

---

## Measurements

### API_MEASUREMENTS_URL

#### Endpoint

`https://renpho.qnclouds.com/api/v2/measurements/list.json`

#### HTTP Method

`GET`

#### Parameters

- `user_id`: (Optional) User ID for fetching weight data.
- `last_at`: Unix timestamp for the oldest data to fetch.
- `locale`: Language/locale setting, usually "en".
- `terminal_user_session_key`: Session key obtained from authentication.

#### Returns

JSON payload containing:

- `last_ary`: Array of most recent measurements for the user.

#### Usage in Code

This URL is used in the `get_measurements()` method to fetch the most recent weight measurements for the user.

## Device Information

### DEVICE_INFO_URL

#### Endpoint

`https://renpho.qnclouds.com/api/v2/device_binds/get_device.json`

#### HTTP Method

`GET`

#### Parameters

- `user_id`: User ID for fetching device information.
- `last_updated_at`: Unix timestamp for the oldest data to fetch.
- `locale`: Language/locale setting, usually "en".
- `terminal_user_session_key`: Session key obtained from authentication.

#### Returns

JSON payload containing:

- `device_info`: Object containing details like device type, device ID, and more.

#### Usage in Code

This URL is used in the `get_device_info()` method to fetch information about the bound device for the user.

#### Data Example

```json
{
  "device_info": {
    "device_type": "Scale",
    "device_id": "abc123",
    "mac_address": "12:34:56:78:90"
  }
}
```

---

## Latest Model Information

### LATEST_MODEL_URL

#### Endpoint

`https://renpho.qnclouds.com/api/v3/devices/list_lastest_model.json`

#### HTTP Method

`GET`

#### Parameters

- `user_id`: User ID for fetching latest model information.
- `last_updated_at`: Unix timestamp for the oldest data to fetch.
- `locale`: Language/locale setting, usually "en".
- `terminal_user_session_key`: Session key obtained from authentication.

#### Returns

JSON payload containing:

- `latest_models`: Array of objects containing latest model details.

#### Usage in Code

This URL is used in the `list_latest_model()` method to fetch the latest model information.

#### Data Example

```json
{
  "latest_models": [
    {
      "model_name": "Renpho Smart Scale",
      "model_id": "xyz789"
    }
  ]
}
```

---

## Girth Information

### GIRTH_URL

#### Endpoint

`https://renpho.qnclouds.com/api/v3/girths/list_girth.json`

#### HTTP Method

`GET`

#### Parameters

- `user_id`: User ID for fetching girth information.
- `last_updated_at`: Unix timestamp for the oldest data to fetch.
- `locale`: Language/locale setting, usually "en".
- `terminal_user_session_key`: Session key obtained from authentication.

#### Returns

JSON payload containing:

- `girths`: Array of objects containing girth measurements for the user.

#### Usage in Code

This URL is used in the `list_girth()` method to fetch the girth measurements for the user.

#### Data Example

```json
{
  "girths": [
    {
      "waist_girth": 30,
      "arm_girth": 12
    }
  ]
}
```

## Girth Goal Information

### GIRTH_GOAL_URL

#### Endpoint

`https://renpho.qnclouds.com/api/v3/girth_goals/list_girth_goal.json`

#### HTTP Method

`GET`

#### Parameters

- `user_id`: User ID for fetching girth goal information.
- `last_updated_at`: Unix timestamp for the oldest data to fetch.
- `locale`: Language/locale setting, usually "en".
- `terminal_user_session_key`: Session key obtained from authentication.

#### Returns

JSON payload containing:

- `girth_goals`: Array of objects containing girth goal measurements for the user.

#### Usage in Code

This URL is used in the `list_girth_goal()` method to fetch the girth goal measurements for the user.

#### Data Example

```json
{
  "girth_goals": [
    {
      "waist_girth_goal": 28,
      "arm_girth_goal": 11
    }
  ]
}
```

---

## Growth Record Information

### GROWTH_RECORD_URL

#### Endpoint

`https://renpho.qnclouds.com/api/v3/growth_records/list_growth_record.json`

#### HTTP Method

`GET`

#### Parameters

- `user_id`: User ID for fetching growth records.
- `last_updated_at`: Unix timestamp for the oldest data to fetch.
- `locale`: Language/locale setting, usually "en".
- `terminal_user_session_key`: Session key obtained from authentication.

#### Returns

JSON payload containing:

- `growth_records`: Array of objects containing growth measurements for the user.

#### Usage in Code

This URL is used in the `list_growth_record()` method to fetch the growth records for the user.

#### Data Example

```json
{
  "growth_records": [
    {
      "height": 175,
      "weight": 70,
      "growth_rate": 1.5
    }
  ]
}
```
