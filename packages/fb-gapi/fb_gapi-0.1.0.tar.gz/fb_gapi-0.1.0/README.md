
# Facebook Messenger Python SDK

A lightweight Python library to send messages via the Facebook Graph API.

## Installation

```
pip install -r requirements.txt
```

## Usage

```python
from facebook_messenger import MessengerClient

ACCESS_TOKEN = "YOUR_FACEBOOK_PAGE_ACCESS_TOKEN"
client = MessengerClient(access_token=ACCESS_TOKEN)

response = client.send_text_message(recipient_id="USER_ID", message_text="Hello from Python!")
print(response)
```

## Error Handling

The library raises `MessengerAPIError` for API-related errors.
