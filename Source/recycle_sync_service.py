import json
import logging
from base64 import b64decode

import config_variables
from recycle_calendar_importer import CalendarImporter

# create logger with 'spam_application'
logger = logging.getLogger('recycle_sync')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('recycle_sync_service.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def decode(encoded: str):
    decoded_bytes = b64decode(encoded)
    return str(decoded_bytes, "utf-8")


if __name__ == "__main__":
    with open("config.json") as json_file:
        config = json.load(json_file)

    logger.info("Config loaded.")

    CalendarImporter.import_calendar(
        config[config_variables.API_SECRET],
        config[config_variables.CITY_ID],
        config[config_variables.STREET_ID],
        config[config_variables.HOUSE_NUMBER],
        config[config_variables.CAL_DAV_URL],
        config[config_variables.USERNAME],
        decode(config[config_variables.PASSWORD]),
        config[config_variables.RECYCLE_CALENDAR_NAME]
    )
