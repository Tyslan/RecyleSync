import argparse
import logging

from caldavutils.recycle_info import RecycleInfo
from recycle_calendar_importer import CalendarImporter

# create logger with 'recycle_sync_cmd'
logger = logging.getLogger('recycle_sync')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('recycle_sync_cmd.log')
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


def get_city_id(info_retriever: RecycleInfo, zip_code: int) -> str:
    cities = info_retriever.get_cities(zip_code)
    return cities[0].id


def get_street_id(info_retriever: RecycleInfo, city_id: str, street_name: str) -> str:
    streets = info_retriever.get_streets(city_id, street_name)
    return streets[0].id


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ApiSecret")
    parser.add_argument("--ZipCode")
    parser.add_argument("--StreetName")
    parser.add_argument("--HouseNr")
    parser.add_argument("--ownCalendarUrl")
    parser.add_argument("--username")
    parser.add_argument("--password")
    parser.add_argument("--recycleCalendarName")

    args = parser.parse_args()

    info_retriever = RecycleInfo(args.ApiSecret)

    city_id = get_city_id(info_retriever, args.ZipCode)
    street_id = get_street_id(info_retriever, city_id, args.StreetName)

    logger.info("Config loaded.")
    CalendarImporter.import_calendar(args.ApiSecret, city_id, street_id, args.HouseNr,
                                     args.ownCalendarUrl, args.username, args.password, args.recycleCalendarName)
