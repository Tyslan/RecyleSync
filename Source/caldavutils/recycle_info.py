import json
import logging
from base64 import b64decode
from datetime import datetime, timedelta

import requests
from ics import Event

from .meta.city import CityRequest
from .meta.event import EventRequest
from .meta.street import StreetRequest

X_CONSUMER_KEY = "x-consumer"
X_CONSUMER_VALUE = "recycleapp.be"
USER_AGENT_KEY = "User-Agent"
USER_AGENT_VALUE = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"

X_SECRET_KEY = "x-secret"
AUTHORIZATION_KEY = "Authorization"

BASE_URL = "https://recycleapp.be/api/app/v1/"

ACCESS_TOKEN_END_POINT = "access-token"


class RecycleInfo():
    def __init__(self, secret: str):
        self.logger = logging.getLogger(
            "recycle_sync.caldavutils.recycle_info.RecycleInfo")

        self.access_token_header = {X_CONSUMER_KEY: X_CONSUMER_VALUE,
                                    X_SECRET_KEY: secret,
                                    USER_AGENT_KEY: USER_AGENT_VALUE
                                    }
        self._sync_access_token()

    def _sync_access_token(self):
        """
        Fills in the request header and updates the expiration date
        """
        self.logger.info("Syncing access token.")
        access_token = self._request_access_token()
        self.request_header = {
            X_CONSUMER_KEY: X_CONSUMER_VALUE,
            AUTHORIZATION_KEY: access_token,
            USER_AGENT_KEY: USER_AGENT_VALUE
        }
        self.access_token_expiration_date = self._get_expiration_date(
            access_token)
        self.logger.info("Access token synced.")

    def _request_access_token(self) -> str:
        response = requests.get(
            f"{BASE_URL}{ACCESS_TOKEN_END_POINT}", headers=self.access_token_header)

        if response is None or response.status_code != 200:
            return []

        json = response.json()
        return json["accessToken"]

    def _get_expiration_date(self, access_token: str) -> datetime:
        """
        Returns the expiration date of the access token in utc time.
        """
        parts = access_token.split('.')
        encoded_time_info = parts[1]
        time_info = self._decode_base64(encoded_time_info)
        expiration_ts = time_info["exp"]
        return datetime.utcfromtimestamp(expiration_ts)

    def _decode_base64(self, encoded_data: str) -> dict:
        ecoded_bytes = b64decode(encoded_data)
        decoded_string = str(ecoded_bytes, "utf-8")
        return json.loads(decoded_string)

    def _access_token_check(self) -> None:
        if self._access_token_expired():
            self._sync_access_token()

    def _access_token_expired(self) -> bool:
        utc_now = datetime.utcnow()
        return utc_now > self.access_token_expiration_date

    def get_cities(self, zip_code: int) -> list:
        request = CityRequest(zip_code)
        json = self._execute_request(request)
        return CityRequest.parse_web_response(json)

    def get_streets(self, zip_code_id: str, query: str) -> list:
        request = StreetRequest(zip_code_id, query)
        json = self._execute_request(request)
        return StreetRequest.parse_web_response(json)

    def get_recycle_events(self, zip_code_id: str, street_id: int, house_number: int, start: datetime, end: datetime, alert: timedelta = timedelta(hours=-6)) -> list:
        request = EventRequest(zip_code_id, street_id,
                               house_number, start, end)
        json = self._execute_request(request)
        events = EventRequest.parse_web_response(json, alert)
        return events

    def _execute_request(self, request) -> dict:
        self._access_token_check()

        response = requests.get(
            f"{BASE_URL}{request.path}", params=request.params, headers=self.request_header)

        if response is None or response.status_code != 200:
            return {}

        return response.json()
