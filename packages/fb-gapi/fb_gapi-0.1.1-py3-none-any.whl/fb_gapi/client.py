import requests
from .exceptions import MessengerAPIError
from .utils import *


class MessengerClient:
    """
    A client for sending messages via the Facebook Messenger Send API.

    Args:
        access_token (str): Your Facebook Page access token.
        api_version (str): Version of the Facebook Graph API to use (default: "v22.0").

    Raises:
        ValueError: If the access token is not provided.
    """

    def __init__(self, access_token: str, api_version: str = "v22.0"):
        if not access_token:
            raise ValueError("An access token must be provided.")
        self.access_token = access_token
        self.api_version = api_version
        self.api_url = f"https://graph.facebook.com/{self.api_version}/me/messages"

    def send_text(self, recipient_id: str, message_text: str) -> dict:
        """
        Sends a plain text message to a Facebook user.

        Args:
            recipient_id (str): The PSID (Page-scoped ID) of the message recipient.
            message_text (str): The text content of the message.

        Returns:
            dict: A JSON response from the Facebook API indicating success or failure.

        Raises:
            MessengerAPIError: If the API responds with an error.
        """
        payload = message_payload(recipient_id, message_text)
        params = {"access_token": self.access_token}
        response = requests.post(self.api_url, params=params, json=payload)
        if response.status_code != 200:
            try:
                error_json = response.json()
            except ValueError:
                error_json = {"error": {"message": response.text}}

            raise MessengerAPIError(response.status_code, error_json)

        return response.json()

    def send_attachment(self, recipient_id: str, image_url: str) -> dict:
        """
        Sends an image attachment to a Facebook user via a publicly accessible URL.

        Args:
            recipient_id (str): The PSID (Page-scoped ID) of the message recipient.
            image_url (str): URL of the image to be sent as an attachment.

        Returns:
            dict: A JSON response from the Facebook API indicating success or failure.

        Raises:
            MessengerAPIError: If the API responds with an error.
        """
        payload = attachment_payload(recipient_id, image_url)
        params = {"access_token": self.access_token}
        response = requests.post(self.api_url, params=params, json=payload)
        if response.status_code != 200:
            try:
                error_json = response.json()
            except ValueError:
                error_json = {"error": {"message": response.text}}

            raise MessengerAPIError(response.status_code, error_json)

        return response.json()
