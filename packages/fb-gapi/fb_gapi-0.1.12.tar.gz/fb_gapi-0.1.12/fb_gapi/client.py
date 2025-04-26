import json
import os
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

    def send_remote_attachment(self, recipient_id: str, image_url: str) -> dict:
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

    def send_local_attachment(self, recipient_id: str, file_path: str) -> dict:
        """
        Sends a local image file to a user by first uploading it and then sending via attachment_id.

        Args:
            recipient_id (str): The PSID of the user.
            file_path (str): The path to the local image file.

        Returns:
            dict: Facebook API response JSON.

        Raises:
            MessengerAPIError: If any part of the upload or message send fails.
        """
        attachment_id = self._upload_image(file_path)
        return self._send_image_by_attachment_id(recipient_id, attachment_id)

    def _upload_image(self, file_path: str) -> str:
        """
        Uploads a local image and returns the attachment_id.

        Args:
            file_path (str): Path to the local image file.

        Returns:
            str: Facebook-generated attachment_id.

        Raises:
            MessengerAPIError: If upload fails.
        """
        url = f"https://graph.facebook.com/{self.api_version}/me/message_attachments"
        params = {"access_token": self.access_token}

        files = {
            "message": (
                None,
                json.dumps(
                    {"attachment": {"type": "image", "payload": {"is_reusable": True}}}
                ),
            ),
            "filedata": (
                os.path.basename(file_path),
                open(file_path, "rb"),
                "image/png",
            ),
            "type": (None, "image/png"),
        }

        try:
            resp = requests.post(url, params=params, files=files)
            resp.raise_for_status()
            data = resp.json()
            attachment_id = data.get("attachment_id")
            if not attachment_id:
                raise MessengerAPIError(resp.status_code, data)
            return attachment_id
        except requests.RequestException as e:
            raise MessengerAPIError(resp.status_code, {"error": {"message": str(e)}})

    def _send_image_by_attachment_id(
        self, recipient_id: str, attachment_id: str
    ) -> dict:
        """
        Sends a message using a previously uploaded image attachment.

        Args:
            recipient_id (str): The PSID of the user.
            attachment_id (str): The image attachment ID from Facebook.

        Returns:
            dict: Facebook API response.

        Raises:
            MessengerAPIError: If sending the message fails.
        """
        url = self.api_url
        params = {"access_token": self.access_token}

        payload = {
            "recipient": {"id": recipient_id},
            "messaging_type": "RESPONSE",
            "message": {
                "attachment": {
                    "type": "image",
                    "payload": {"attachment_id": attachment_id},
                }
            },
        }

        response = requests.post(url, params=params, json=payload)
        if response.status_code != 200:
            try:
                error_json = response.json()
            except ValueError:
                error_json = {"error": {"message": response.text}}

            raise MessengerAPIError(response.status_code, error_json)

        return response.json()
