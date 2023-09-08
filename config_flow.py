import voluptuous as vol
from homeassistant import config_entries, data_entry_flow

from const import DOMAIN, CONF_USER_ID, CONF_PUBLIC_KEY, CONF_EMAIL, CONF_PASSWORD
from RenphoWeight import RenphoWeight

class RenphoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

async def async_step_user(self, user_input=None):
    """Handle a flow initialized by the user."""
    errors = {}

    # Define the schema and set default values and descriptions
    schema = vol.Schema({
            vol.Required(CONF_EMAIL, description={"suggested_value": "Your email"}): str,
            vol.Required(CONF_PASSWORD, description={"suggested_value": "Your password"}): str,
            vol.Optional(CONF_USER_ID, description={"suggested_value": "Optional User ID"}): str,
        })

    if user_input is not None:
        email = user_input[CONF_EMAIL]
        password = user_input[CONF_PASSWORD]
        user_id = user_input.get(CONF_USER_ID, None)

        # Initialize your Renpho object
        renpho = RenphoWeight(CONF_PUBLIC_KEY, email, password, user_id)

        # Preliminary validation; replace with your validation logic
        try:
            is_valid = await renpho.validate_credentials()
        except Exception as e:
            _LOGGER.error("Validation failed: %s", str(e))
            is_valid = False

        if is_valid:
            return self.async_create_entry(
                title=email,
                data={
                    CONF_EMAIL: email,
                    CONF_PASSWORD: password,
                    CONF_USER_ID: user_id,
                },
            )
        else:
            errors["base"] = "invalid_auth"

    # Use the schema defined above in the form
    return self.async_show_form(
        step_id="user",
        data_schema=schema,
        errors=errors,
    )