from caldav import Calendar, Principal

from .calendar_wrapper import CalendarWrapper


class PrincipalWrapper:
    def __init__(self, principal: Principal):
        self._principal = principal

    def get_all_calendars(self) -> list:
        return self._principal.calendars()

    def get_calendar_by_name(self, name: str) -> Calendar:
        for calendar in self.get_all_calendars():
            if calendar.name == name:
                return calendar
        return None

    def add_new_calendar(self, name: str) -> None:
        self._principal.make_calendar(name=name)
