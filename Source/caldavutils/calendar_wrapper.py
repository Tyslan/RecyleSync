from datetime import datetime

from caldav import Calendar, Event
from ics import Calendar as IcsCalendar, Event as IcsEvent


class CalendarWrapper:
    def __init__(self, calendar: Calendar):
        self._calendar = calendar

    def get_events_between(self, start: datetime, end: datetime) -> list:
        return self._calendar.date_search(start, end)

    def get_all_events(self) -> list:
        return self._calendar.events()

    def update(self, event: Event) -> None:
        event.update()

    def delete_all_events(self) -> None:
        events = self.get_all_events()
        for event in events:
            self.delete(event)

    def delete_events_between(self, start: datetime, end: datetime) -> None:
        events = self.get_events_between(start, end)
        for event in events:
            self.delete(event)

    def delete(self, event: Event) -> None:
        event.delete()

    def add_event(self, event: IcsEvent) -> None:
        cal = IcsCalendar()
        cal.events.add(event)
        event_data = str(cal)
        self._calendar.add_event(event_data)

    def add_events(self, events: list) -> None:
        for event in events:
            self.add_event(event)
