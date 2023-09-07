from src.__init__ import setup


def setup(hass, config):
    return src.setup(hass, config)

if __name__ == "__main__":
    # This code is executed when running this file directly
    # It is used for testing purposes
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from src.RenphoWeight import RenphoWeight
    from src.const import CONF_PUBLIC_KEY
    import logging
    logging.basicConfig(level=logging.DEBUG)
    renpho = RenphoWeight(CONF_PUBLIC_KEY, '<username>', '<password>', '<user_id>')
    renpho.startPolling(10)
    print(renpho.getScaleUsers())
    print(renpho.getSpecificMetricFromUserID("bodyfat"))
    print(renpho.getSpecificMetricFromUserID("bodyfat", "<user_id>"))
    print(renpho.getInfo())
    input("Press Enter to stop polling")
    renpho.stopPolling()