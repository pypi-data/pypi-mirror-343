# Securden Software Development Kit - Python

This guide will take you through the process of installing and integrating Securden Python SDK for secure programmatic access to credentials.

## Summary of Steps

1. Installation
3. Fetch credential using pre-defined commands

## 1. Installation

```hcl
pip install securden_sdk
```

## 3. Fetch credential via CLI commands

### Required

- `server_url` (String) Securden Server URL. Example: https://company.securden.com:5454.
- `authtoken` (String) Securden API Authentication Token.

```hcl
from securden_sdk import ApiClient
from securden_sdk import Configuration
from securden_sdk.api import DefaultApi 

config = Configuration(
    host="<your_securden_server_url>",
)
api = ApiClient(configuration=config)
api.authtoken = "<your_api_key>"
securden_instance = DefaultApi(api)

try:
    password = securden_instance.get_password(account_id=<your_account_id>)
    print("Response:", password)
except Exception as e:
    print(e)
```

---
-> If you have general questions or issues in using Securden SDK, you may raise a support request to devops-support@securden.com. Our support team will get back to you at the earliest and provide a timeline if there are issue fixes involved.