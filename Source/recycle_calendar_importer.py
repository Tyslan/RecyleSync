import logging
from datetime import datetime

import pytz
from caldav import DAVClient
from dateutil.relativedelta import relativedelta

from caldavutils.calendar_wrapper import CalendarWrapper
from caldavutils.principal_wrapper import PrincipalWrapper
from caldavutils.recycle_info import RecycleInfo


class CalendarImporter:
    logger = logging.getLogger(
        "recycle_sync.recycle_calendar_importer.CalendarImporter")

    IMPORTER_TIME_ZONE = pytz.timezone('Europe/Brussels')

    @staticmethod
    def import_calendar(api_secret: str, city_id: str, street_id: str, house_nr: int, caldav_url: str, username: str, password: str, recycle_calendar_name: str):
        dav_client = DAVClient(url=caldav_url,
                               username=username, password=password)
        recycle_calendar = CalendarImporter._get_recycle_calendar(
            dav_client, recycle_calendar_name)

        first_of_month = CalendarImporter._get_first_day_of_current_month()
        next_month = CalendarImporter._add_month(first_of_month, 2)
        previous_month = CalendarImporter._substract_month(first_of_month, 1)

        info_retriever = RecycleInfo(api_secret)

        CalendarImporter.logger.info(
            f"Retrieving all events between {previous_month.isoformat()} and {next_month.isoformat()} from the API")
        events = info_retriever.get_recycle_events(
            city_id, street_id, house_nr, previous_month, next_month)

        CalendarImporter.logger.info(
            f"Deleting all events older than {previous_month.isoformat()}.")
        recycle_calendar.delete_events_between(
            datetime(1970, 1, 1), next_month)

        CalendarImporter.logger.info(
            f"Adding {len(events)} newly fetched events.")
        recycle_calendar.add_events(events)
        CalendarImporter.logger.info("Succesfully finished.")

    @staticmethod
    def _get_recycle_calendar(dav_client: DAVClient, recycle_calendar_name: str) -> CalendarWrapper:
        principal = PrincipalWrapper(dav_client.principal())

        recycle_calendar = principal.get_calendar_by_name(
            recycle_calendar_name)
        if not recycle_calendar:
            principal.add_new_calendar(recycle_calendar_name)
            recycle_calendar = principal.get_calendar_by_name(
                recycle_calendar_name)
        return CalendarWrapper(recycle_calendar)

    @staticmethod
    def _get_first_day_of_current_month() -> datetime:
        now = datetime.now()
        first_of_month = datetime(now.year, now.month, 1)
        return CalendarImporter.IMPORTER_TIME_ZONE.localize(first_of_month)

    @staticmethod
    def _add_month(date: datetime, month_diff: int) -> datetime:
        diff = relativedelta(months=month_diff)
        return date + diff

    @staticmethod
    def _substract_month(date: datetime, month_diff: int) -> datetime:
        diff = relativedelta(months=month_diff)
        return date - diff
