import asyncio
import logging

from httpcore import TimeoutException

from .const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_PUBLIC_KEY,
    CONF_REFRESH,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_USER_ID,
    DOMAIN,
    EVENT_HOMEASSISTANT_STOP,
)
from .api_renpho import RenphoWeight


# Initialize logger
_LOGGER = logging.getLogger(__name__)

# ------------------- Setup Methods -------------------


async def async_setup(hass, config):
    """Set up the Renpho component from YAML configuration."""
    _LOGGER.debug("Starting hass_renpho")

    if conf := config.get(DOMAIN):
        await setup_renpho(hass, conf)
    return True


async def async_setup_entry(hass, entry):
    """Set up Renpho from a config entry."""
    await setup_renpho(hass, entry.data)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    # Remove Renpho instance if it exists
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if DOMAIN in hass.data:
        del hass.data[DOMAIN]
        return True


# ------------------- Helper Methods -------------------

async def setup_renpho(hass, conf):
    """Common setup logic for YAML and UI."""
    email = conf[CONF_EMAIL]
    password = conf[CONF_PASSWORD]
    unit_of_measurement = conf.get(CONF_UNIT_OF_MEASUREMENT, "kg")
    user_id = conf.get(CONF_USER_ID)
    refresh = conf.get(CONF_REFRESH, 60)
    renpho = RenphoWeight(
        email=email,
        password=password,
        user_id=user_id,
        refresh=refresh,
    )

    hass.data[DOMAIN] = renpho

    hass.data[DOMAIN] = renpho
    hass.data[CONF_EMAIL] = email
    hass.data[CONF_USER_ID] = user_id
    hass.data[CONF_REFRESH] = refresh
    hass.data[CONF_UNIT_OF_MEASUREMENT] = unit_of_measurement

    return True



# ------------------- Main Method for Testing -------------------

if __name__ == "__main__":

    async def main():
        import os
        from dotenv import load_dotenv

        load_dotenv()

        email = os.environ.get("EMAIL")
        password = os.environ.get("PASSWORD")
        user_id = os.environ.get("USER_ID", None)

        renpho = RenphoWeight(CONF_PUBLIC_KEY, email, password, user_id)

        try:
            await renpho.auth()
            print("Authentication successful.")

            await renpho.get_info()
            print("Fetched user info.")

            users = await renpho.get_scale_users()
            print("Fetched scale users:", users)

            measurements = await renpho.get_measurements()
            print("Fetched measurements:", measurements)

            weight = await renpho.get_weight()
            print("Fetched weight:", weight[0])

            specific_metric = await renpho.get_specific_metric('weight', 'weight')
            print(f"Fetched specific metric: {specific_metric}")

            # await renpho.start_polling(refresh=1)
            # print("Started polling.")

            # await renpho.stop_polling()
            # print("Stopped polling.")

            device_info = await renpho.get_device_info()
            print("Fetched device info:", device_info)

            latest_model = await renpho.list_latest_model()
            print("Fetched latest model:", latest_model)

            girth_info = await renpho.list_girth()
            print("Fetched girth info:", girth_info)

            girth_goal = await renpho.list_girth_goal()
            print("Fetched girth goal:", girth_goal)

            growth_record = await renpho.list_growth_record()
            print("Fetched growth record:", growth_record)

            messages = await renpho.message_list()
            print("Fetched message list:", messages)

            # request_user = await renpho.request_user()
            # print("Fetched request user:", request_user)

            # reach_goal = await renpho.reach_goal()
            # print("Fetched reach_goal:", reach_goal)

        except Exception as e:
            print(f"An exception occurred: {e}")

        finally:
            input("Press Enter to stop polling")
            await renpho.close()  # This method also stops polling as per your class definition

    asyncio.run(main())
