# config_flow.py

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant

from .const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_PUBLIC_KEY,
    CONF_REFRESH,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_USER_ID,
    DOMAIN,
    MASS_KILOGRAMS,
    MASS_POUNDS,
)
from .api_renpho import RenphoWeight

_LOGGER = logging.getLogger(__name__)


DATA_SCHEMA = vol.Schema(
    {
        vol.Required(
            CONF_EMAIL, description={"suggested_value": "example@email.com"}
        ): str,
        vol.Required(CONF_PASSWORD, description={"suggested_value": "Password"}): str,
        vol.Optional(
            CONF_USER_ID, description={"suggested_value": "OptionalUserID"}
        ): str,
        vol.Optional(CONF_REFRESH, description={"suggested_value": 60}): int,
        vol.Optional(CONF_UNIT_OF_MEASUREMENT, default=MASS_KILOGRAMS): vol.In(
            [MASS_KILOGRAMS, MASS_POUNDS]
        ),
    }
)


async def async_validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    _LOGGER.debug("Starting to validate input: %s", data)
    user_id = data.get(CONF_USER_ID)
    if data.get(CONF_USER_ID) == "OptionalUserID":
        user_id = None
    renpho = RenphoWeight(
        CONF_PUBLIC_KEY,
        data[CONF_EMAIL],
        data[CONF_PASSWORD],
        user_id,
        data.get(CONF_REFRESH, 60),
    )
    is_valid = await renpho.validate_credentials()
    if not is_valid:
        raise CannotConnect(
            reason="Invalid credentials",
            details={
                "email": data[CONF_EMAIL],
            },
        )
    return {"title": data[CONF_EMAIL]}


class RenphoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                info = await async_validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)

            except CannotConnect as e:
                errors["base"] = "cannot_connect"
                _LOGGER.error(
                    f"Cannot connect due to {e.reason}. Details: {e.get_details()}"
                )

            except exceptions.HomeAssistantError as e:
                errors["base"] = "home_assistant_error"
                _LOGGER.error(f"Home Assistant specific error: {str(e)}")

            except Exception as e:  # pylint: disable=broad-except
                errors["base"] = "unknown_error"
                _LOGGER.exception(f"Unexpected exception: {e}")

        # Use description_placeholders for dynamic info
        placeholders = {
            "additional_info": "Please provide your Renpho login details.",
            "icon": "renpho.png",
            "description": "This is a description of your Renpho integration.",
        }

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
            description_placeholders=placeholders,
        )


class CannotConnect(exceptions.HomeAssistantError):
    def __init__(self, reason: str = "", details: dict = None):
        super().__init__(self)
        self.reason = reason
        self.details = details or {}

    def __str__(self):
        return f"CannotConnect: {self.reason}"

    def get_details(self):
        return self.details
