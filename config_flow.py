from __future__ import annotations
import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_USER_ID, CONF_PUBLIC_KEY, CONF_EMAIL, CONF_PASSWORD
from .RenphoWeight import RenphoWeight

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_EMAIL, description={"suggested_value": "example@email.com"}): str,
    vol.Required(CONF_PASSWORD, description={"suggested_value": "Password"}): str,
    vol.Optional(CONF_USER_ID, description={"suggested_value": "OptionalUserID"}): str,
})

async def async_validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    _LOGGER.debug("Starting to validate input: %s", data)
    renpho = RenphoWeight(CONF_PUBLIC_KEY, data[CONF_EMAIL], data[CONF_PASSWORD], data.get(CONF_USER_ID, None))
    is_valid = await renpho.validate_credentials()
    if not is_valid:
        raise CannotConnect(reason="Invalid credentials", details={"email": data[CONF_EMAIL], "user_id": data.get(CONF_USER_ID, None)})
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
                _LOGGER.error("Cannot connect: %s, details: %s", e.reason, e.get_details())
                errors["base"] = "cannot_connect"
            except exceptions.HomeAssistantError as e:
                _LOGGER.error("Home Assistant specific error: %s", str(e))
                errors["base"] = "home_assistant_error"
            except Exception as e:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception: %s", e)
                errors["base"] = "unknown_error"
        
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA.extend({vol.Set(user_input)} if user_input else {}),  # Prefill form
            errors=errors,
            description_placeholders={
                "additional_info": "Please provide your Renpho login details.",
                "icon": "renpho.png",  # Replace with your actual icon path
                "description": "This is a description of your Renpho integration."
            },
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
