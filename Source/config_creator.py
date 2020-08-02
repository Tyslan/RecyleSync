import json
from base64 import b64encode
from getpass import getpass

import config_variables
from caldavutils.recycle_info import RecycleInfo


def get_city_id(info_retriever: RecycleInfo, zip_code: int, cities: list = None) -> str:
    if not cities:
        cities = info_retriever.get_cities(zip_code)
    for i, city in enumerate(cities):
        print(f"{i+1}: {city.name}")
    selection = input("Select city from list: ")
    selection = int(selection)
    if selection > len(cities) or selection <= 0:
        print("Invalid selection. Try again...")
        return get_city_id(info_retriever, zip_code, cities)
    city = cities[selection - 1]
    return city.id


def get_street_id(info_retriever: RecycleInfo, city_id: str, street_name: str, streets: list = None) -> str:
    if not streets:
        streets = info_retriever.get_streets(city_id, street_name)
    for i, city in enumerate(streets):
        print(f"{i+1}: {city.name}")
    selection = input("Select street from list: ")
    selection = int(selection)
    if selection > len(streets) or selection <= 0:
        print("Invalid selection. Try again...")
        return get_street_id(info_retriever, zip_code, street_name, streets)
    street = streets[selection - 1]
    return street.id


def get_password() -> str:
    return encode_base64(getpass())


def encode_base64(password: str) -> str:
    encoded_bytes = b64encode(password.encode("utf-8"))
    return str(encoded_bytes, "utf-8")


api_secret = input("What is your API secret for recycleapp.be? ")

info_retriever = RecycleInfo(api_secret)
zip_code = input("What is your zip code? ")
city_id = get_city_id(info_retriever, zip_code)
print(city_id)

street_name = input("What is your street name? ")
street_id = get_street_id(info_retriever, city_id, street_name)
print(street_id)

house_number = input("What is your house number? ")
destination_calendar = input("What is your destination calendar base url? ")
user_name = input("What is your username? ")
password = get_password()
recycle_calender_name = input("What is your recycle calendars name? ")

config = {
    config_variables.API_SECRET: api_secret,
    config_variables.CITY_ID: city_id,
    config_variables.STREET_ID: street_id,
    config_variables.HOUSE_NUMBER: house_number,
    config_variables.CAL_DAV_URL: destination_calendar,
    config_variables.USERNAME: user_name,
    config_variables.PASSWORD: password,
    config_variables.RECYCLE_CALENDAR_NAME: recycle_calender_name
}

with open('config.json', 'w') as fp:
    json.dump(config, fp, indent=4)
