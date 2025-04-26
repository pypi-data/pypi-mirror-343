import requests
from .exceptions import MessengerAPIError
from .utils import *


class MessengerClient:
    def __init__(self, access_token: str, api_version: str = "v22.0"):
        if not access_token:
            raise ValueError("An access token must be provided.")
        self.access_token = access_token
        self.api_version = api_version
        self.api_url = f"https://graph.facebook.com/{self.api_version}/me/messages"

    def send_text(self, recipient_id: str, message_text: str):
        payload = message_payload(recipient_id, message_text)
        params = {"access_token": self.access_token}
        response = requests.post(self.api_url, params=params, json=payload)
        if response.status_code != 200:
            raise MessengerAPIError(f"Error {response.status_code}: {response.text}")
        return response.json()

    def send_attachment(self, recipient_id: str, image_url: str):
        payload = attachment_payload(recipient_id, image_url)
        params = {"access_token": self.access_token}
        response = requests.post(self.api_url, params=params, json=payload)
        if response.status_code != 200:
            raise MessengerAPIError(f"Error {response.status_code}: {response.text}")
        return response.json()
