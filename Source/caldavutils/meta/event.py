from datetime import datetime, timedelta
from dateutil import parser

import pytz
from ics import Event
from ics.alarm import DisplayAlarm

EVENT_END_POINT = "collections"
ZIP_CODE_ID = "zipcodeId"
STREET_ID = "streetId"
HOUSE_NR = "houseNumber"
START = "fromDate"
END = "untilDate"

TIME_FORMAT_ENTRY = "%Y-%m-%d"
TIME_ZONE_RESULT = pytz.timezone('Europe/Brussels')


def parse_date_time(ts: datetime) -> str:
    return ts.strftime(TIME_FORMAT_ENTRY)


def parse_ts(ts: str, tz=TIME_ZONE_RESULT) -> datetime:
    result = parser.parse(ts)
    result = result.replace(tzinfo=None)
    result = tz.localize(result)
    return result


def _create_event(timestamp: str, name: str, alert: timedelta):
    date = parse_ts(timestamp)
    datestr = date.isoformat()
    alarm = None
    if alert:
        alarm = DisplayAlarm(trigger=alert, display_text=name)
    event = Event(name=name, begin=datestr, alarms=[alarm])
    return event


class EventRequest:

    def __init__(self, zip_code_id: str, street_id: int, house_number: int, start: datetime, end: datetime):
        start_param = parse_date_time(start)
        end_param = parse_date_time(end)
        self.params = {ZIP_CODE_ID: zip_code_id, STREET_ID: street_id, HOUSE_NR: house_number,
                       START: start_param, END: end_param}
        self.path = EVENT_END_POINT

    @ classmethod
    def parse_web_response(cls, response: dict, alarm_reminder: timedelta = None, language: str = "nl") -> list:
        items = response["items"]
        result = []
        for item in items:
            ts = item["timestamp"]
            fraction = item["fraction"]
            names = fraction["name"]
            name = names[language]
            event = _create_event(ts, name, alarm_reminder)
            result.append(event)

        return result
