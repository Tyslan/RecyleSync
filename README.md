# RecyleSync

Sync Belgian waste calendars with a CalDav server

## Config variables

- x-secret: determine from observing webpage [https://recycleapp.be/calendar](https://recycleapp.be/calendar) with developer tools, specifically look for the request https://recycleapp.be/api/app/v1/access-token

## Determine the base url of own calendar

[Source](https://www.ict4g.net/adolfo/notes/admin/determining-url-of-caldav-calendars.html)

## CalDav and ics

For communication with CalDav, the following library is used: [caldav](https://github.com/python-caldav/caldav)

For ics the following library is used: [ics](https://icspy.readthedocs.io/en/stable/)

## TODO

### Google

Google doesn't allow to access caldav urls: have a look at [calendar quickstart](https://developers.google.com/calendar/quickstart/pytho
