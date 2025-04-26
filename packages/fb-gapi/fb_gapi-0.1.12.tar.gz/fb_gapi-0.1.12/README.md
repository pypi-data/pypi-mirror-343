
# Facebook Messenger Graph API Python SDK

A lightweight Python SDK for sending messages (text and image attachments) using the Facebook Graph API.

## 🚀 Usage
### 📦 Import the client
```python
from facebook_messenger import MessengerClient
```

### 🔒 Initialize with your Page Access Token 
```python
client = MessengerClient(access_token="YOUR_PAGE_ACCESS_TOKEN")
```


### ✉️ Sending a Text Message
```python
response = client.send_text(recipient_id="USER_PSID", message_text="Hello, user!")
print(response)
```

### 🖼️ Sending an Image Attachment
```python
image_url = "https://example.com/image.jpg"
response = client.send_attachment(recipient_id="USER_PSID", image_url=image_url)
print(response)
```


### ⚠️ Error Handling
This SDK will raise a `MessengerAPIError` when the Facebook API responds with an error.

### Example:
```python
from facebook_messenger import MessengerAPIError

try:
    client.send_text("invalid_user_id", "Hi!")
except MessengerAPIError as e:
    print(f"GAPI Error: {e}")
```

### Error Output Example:
```
MessengerAPIError (HTTP 400): [OAuthException] Invalid OAuth access token. (code 190)
```


## 📄 Requirements
- **Python 3.6+**



## 🛠️ TODO
- **Add support for other templates.**
- **Support for quick replies, actions, and custom buttons.**


## 📃 License
MIT License. Use freely and contribute!
