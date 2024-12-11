# tinder_api.py

import requests

class TinderAPI:
    def __init__(self, token):
        self._token = token
        self.base_url = "https://api.gotinder.com"
        self.headers = {
            "X-Auth-Token": self._token,
            "Content-Type": "application/json"
        }

    def profile(self):
        response = requests.get(
            f"{self.base_url}/v2/profile?include=account%2Cuser",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def matches(self, limit=20):
        response = requests.get(
            f"{self.base_url}/v2/matches?count={limit}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()["data"]["matches"]

    def get_messages(self, match_id):
        response = requests.get(
            f"{self.base_url}/v2/matches/{match_id}/messages?count=100",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()["data"]["messages"]

    def send_message(self, match_id, message):
        payload = {"message": message}
        response = requests.post(
            f"{self.base_url}/user/matches/{match_id}",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
