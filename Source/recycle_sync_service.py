import json
from base64 import b64decode

import config_variables
from recycle_calendar_importer import CalendarImporter


def decode(encoded: str):
    decoded_bytes = b64decode(encoded)
    return str(decoded_bytes, "utf-8")


if __name__ == "__main__":
    with open("config.json") as json_file:
        config = json.load(json_file)
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
