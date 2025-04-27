import json
import os


def message_payload(recipient_id: int, message_text: str) -> dict:
    """
    Build a JSON payload for sending a simple text message via Facebook Messenger.

    Args:
        recipient_id (str): The PSID (Page-scoped ID) of the message recipient.
        message_text (str): The text content of the message to be sent.

    Returns:
        dict: A dictionary representing the JSON payload, structured for the Send API.
    """
    return {
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
    }


def attachment_payload_remote(recipient_id: int, attachment_url: str) -> dict:
    """
    Build a JSON payload for sending an image attachment via Facebook Messenger.

    Args:
        recipient_id (str): The PSID (Page-scoped ID) of the message recipient.
        attachment_url (str): The URL of the image to send as an attachment.

    Returns:
        dict: A dictionary representing the JSON payload for an image message.
    """
    return {
        "messaging_type": "RESPONSE",
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {"type": "image", "payload": {"url": attachment_url}}
        },
    }


def attachment_upload_local(file_path):
    """
    Build a multipart/form-data payload for uploading an image via Facebook Messenger.

    Args:
        file_path (str): The local path to the image file.

    Returns:
        dict: A dictionary representing the multipart/form-data payload.
    """
    return {
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


def attachment_payload_local(recipient_id: int, attachment_id: str) -> dict:
    """
    Build a JSON payload for sending an image attachment via Facebook Messenger using an attachment_id.

    Args:
        recipient_id (str): The PSID (Page-scoped ID) of the message recipient.
        attachment_id (str): The attachment_id returned from the Facebook attachment API.

    Returns:
        dict: A dictionary representing the JSON payload for an image message.
    """
    return {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {
            "attachment": {
                "type": "image",
                "payload": {"attachment_id": attachment_id},
            }
        },
    }


def extract_chat_messages(user_id: int, fb_json: dict) -> list:
    """
    Extracts chat messages from the Facebook API response JSON.

    Args:
        user_id (int): The PSID of the user whose messages we want to extract.
        fb_json (dict): JSON response from the Facebook Conversations API.

    Returns:
        list: A list of dictionaries with 'sender' and 'message' keys, representing the extracted chat messages.
    """
    messages_list = [
        {
            "sender": "user" if msg.get("from", {}).get("id") == user_id else "page",
            "message": msg.get("message", ""),
        }
        for conv in fb_json.get("data", [])
        for msg in conv.get("messages", {}).get("data", [])
        if not user_id
        or str(msg.get("from", {}).get("id")) == str(user_id)
        or user_id is None
    ]

    return messages_list
