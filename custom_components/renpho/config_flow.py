from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant

from homeassistant.helpers import translation

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

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_EMAIL): str,
    vol.Required(CONF_PASSWORD): str,
    vol.Optional(CONF_REFRESH, default=60): int,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT, default=MASS_KILOGRAMS): vol.In([MASS_KILOGRAMS, MASS_POUNDS]),
    vol.Optional("proxy"): str
})

async def async_validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    _LOGGER.debug("Starting to validate input: %s", data)
    renpho = RenphoWeight(
        email=data[CONF_EMAIL],
        password=data[CONF_PASSWORD],
        refresh=data.get(CONF_REFRESH, 60),
        proxy=data.get("proxy", None)
    )
    is_valid = await renpho.validate_credentials()
    if not is_valid:
        raise CannotConnect(
            reason="Invalid credentials",
            details={
                "email": data[CONF_EMAIL],
            },
        )

    await renpho.get_scale_users()

    user_ids = [
        user.get("user_id", None)
        for user in renpho.users
    ]

    if not user_ids:
        raise CannotConnect(reason="No users found", details={"email": data[CONF_EMAIL]})

    return {"title": data[CONF_EMAIL], "user_ids": user_ids, "renpho_instance": renpho}

class RenphoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                info = await async_validate_input(self.hass, user_input)
                self.renpho_temp_data = user_input
                self.renpho_instance = info["renpho_instance"]
                self.user_ids = info["user_ids"]

                if len(self.user_ids) > 1:
                    return await self.async_step_select_user()
                self.renpho_temp_data[CONF_USER_ID] = self.user_ids[0]
                return self.async_create_entry(title=info["title"], data=self.renpho_temp_data)

            except CannotConnect as e:
                errors["base"] = "cannot_connect"
                _LOGGER.error(f"Cannot connect due to {e.reason}. Details: {e.get_details()}")

            except Exception as e:  # pylint: disable=broad-except
                errors["base"] = "unknown_error"
                _LOGGER.exception(f"Unexpected exception: {e}")

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors
        )

    async def async_step_select_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            self.renpho_temp_data[CONF_USER_ID] = user_input[CONF_USER_ID]
            data[CONF_USER_ID] = user_input[CONF_USER_ID]
            return self.async_create_entry(title=self.renpho_temp_data[CONF_EMAIL], data=self.renpho_temp_data)

        user_id_schema = vol.Schema({
            vol.Required(CONF_USER_ID, description={"suggested_value": self.user_ids[0]}): vol.In(self.user_ids),
        })

        return self.async_show_form(
            step_id="select_user",
            data_schema=user_id_schema,
            errors=errors,
            description_placeholders={"additional_info": "Please select your User ID."}
        )

class CannotConnect(exceptions.HomeAssistantError):
    def __init__(self, reason: str = "", details: dict = None):
        super().__init__()
        self.reason = reason
        self.details = details or {}

    def __str__(self):
        return f"CannotConnect: {self.reason} - {self.details}"

    def get_details(self):
        return self.details
