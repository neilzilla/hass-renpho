# Renpho Weight Scale Integration for Home Assistant

## About

This custom component allows you to seamlessly integrate Renpho's weight scale into Home Assistant. Get real-time updates on your weight, BMI, body fat percentage, and other health metrics right on your Home Assistant dashboard.

![Renpho Weight Scale](renpho.png)

## Features

- **Real-Time Health Metrics**: Fetches weight, BMI, body fat, and other health metrics.
- **User-Friendly**: Easily configurable via the Home Assistant UI.
- **Multi-User Support**: Supports tracking metrics for multiple users.
- **Automations**: Use your health metrics in automations, like sending alerts or updating other connected devices.

## Installation

### 1. Prerequisites

- Make sure you have [HACS](https://hacs.xyz/) installed.

### 2. Install the Custom Component Using Custom Repository

- Open HACS in your Home Assistant instance.
- Click on "Integrations" from the sidebar.
- Click on the "Custom Repositories" button in the top right corner.
- Enter the URL of this GitHub repository, select "Integration" as the category, and then click "Add".
- Once the repository is added, it will appear in the "Integrations" tab. Click "Install" to install the custom component.

### 3. Configuration

- Navigate to **Configuration > Integrations > Add Integration**.
- Search for `Renpho` and click to add.
- Provide your Renpho account email, password, and optionally a `user_id`.
- Set the refresh rate in milliseconds for how often you want to poll for updates.

## Configuration/Customization

### 1. User ID (Optional)

If you're using this integration for multiple users, each user should have a unique `user_id`.

### 2. Refresh Rate

Set how often the component should fetch new data from the Renpho servers. Note: A too frequent refresh rate may result in rate limiting.

## Support

For issues, feature requests or further assistance, head over to our [GitHub Repository](https://github.com/antoinebou12/hass_renpho/issues).

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/antoinebou12/hass_renpho?color=41BDF5&style=for-the-badge)](https://github.com/antoinebou12/hass_renpho/releases/latest)
[![Integration Usage](https://img.shields.io/badge/dynamic/json?color=41BDF5&style=for-the-badge&logo=home-assistant&label=usage&suffix=%20installs&cacheSeconds=15600&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.hass_renpho.total)](https://analytics.home-assistant.io/)

## Contributors

- [@antoinebou12](https://github.com/antoinebou12)

## Acknowledgments

Inspired by other health metric integrations and the Home Assistant community.

For more details, please refer to the [Documentation](https://github.com/antoinebou12/hass_renpho).