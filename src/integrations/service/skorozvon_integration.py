from datetime import datetime, timedelta

import requests

from django.conf import settings

from ..service.exceptions import SkorozvonAPIError


class SkorozvonAPI:
    _token = None
    BASE_URL = "https://app.skorozvon.ru/api/v2/"

    def __init__(self):
        self._token = self._get_token()

    @staticmethod
    def _get_token():
        # TODO: cache token
        url = "https://app.skorozvon.ru/oauth/token"
        data = {
            "grant_type": "password",
            "username": settings.SKOROZVON_LOGIN,
            "api_key": settings.SKOROZVON_API_KEY,
            "client_id": settings.SKOROZVON_APPLICATION_ID,
            "client_secret": settings.SKOROZVON_APPLICATION_KEY,
        }
        token = requests.post(url, data=data).json()
        return f"Bearer {token['access_token']}"

    def _get_request(self, endpoint_url, params=None, has_content=False):
        headers = {
            "Authorization": self._token
        }
        response = requests.get(self.BASE_URL + endpoint_url, params=params, headers=headers)
        if has_content:
            return response.content
        try:
            return response.json()
        except Exception as e:
            return None

    def get_call_audio(self, call_id: int):
        return self._get_request(f"calls/{call_id}.mp3", has_content=True)

    def get_scenarios(self):
        response = self._get_request("scenarios")
        if not response:
            raise SkorozvonAPIError("Skorozvon dont return anything")
        return {sc["id"]: sc["name"] for sc in response["data"]}

    def get_users(self):
        users = self._get_request("users")
        if not users:
            raise SkorozvonAPIError("Skorozvon dont return anything")
        return {user.get("id", ""): user.get("name", "") for user in users}

    def get_call_report(self):
        params = {
            "length": 5,
            "start_time": int(datetime.timestamp(datetime.now())),
            "end_time": int(datetime.timestamp(datetime.now() - timedelta(days=1))),
            "page": 1,
            "selected_fields": "all",
            "filter": {
                "results_ids": "all",
                "scenarios_ids": "all",
                "types": "all",
                "users_ids": "all"
            }
        }
        headers = {
            "Authorization": self._token
        }
        url = 'https://api.skorozvon.ru/api/reports/calls_total'
        data = requests.get(url=url, headers=headers, params=params)
        print(data)
        print(data.text)
        return {}


skorozvon_api = SkorozvonAPI()
