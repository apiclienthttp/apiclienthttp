# API Client HTTP

Client for sync/async query HTTP API Services.
It provides a high-level interface for managing URLs, headers, and authentication.
Based on [HTTPX](https://github.com/encode/httpx) library.

## Features

- Synchronous and asynchronous HTTP requests
- Token-based authentication
- Customizable headers
- URL management
- Error handling

## Installation

To install the library, use pip:

```bash
pip install api-client-http
```

## Usage

### Synchronous client

```python
from api_client_http import RestClient
from api_client_http.auth import TokenAuth

client = RestClient(
    address="https://api.example.com/v1",
    endpoints= {
      'token': 'auth/token',
      'query': 'query/{}'
    }
)

auth_respone = client.post('token', json={'username': 'user', 'password': 'password'})
response = client.get('query', '123', auth=TokenAuth(auth_respone['access_token']))
```

### Asynchronous client

```python
from api_client_http import AsyncRestClient
from api_client_http.auth import TokenAuth

client = AsyncRestClient(
    address="https://api.example.com/v1",
    endpoints= {
      'token': 'auth/token',
      'query': 'query/{}'
    }
)

auth_respone = await client.post('token', json={'username': 'user', 'password': 'password'})
response = await client.get('query', '123', auth=TokenAuth(auth_respone['access_token']))
```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
