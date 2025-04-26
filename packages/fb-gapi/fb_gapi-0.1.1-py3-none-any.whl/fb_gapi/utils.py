def message_payload(recipient_id: str, message_text: str) -> dict:
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


def attachment_payload(recipient_id: str, attachment_url: str) -> dict:
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
