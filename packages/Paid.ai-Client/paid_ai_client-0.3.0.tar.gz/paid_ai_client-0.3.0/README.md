# Paid Client

A Python client for interacting with the Paid API. This package allows you to send transaction events to the API.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Paid.ai-Client.

```bash
pip install Paid.ai-Client
```

## Usage

```python
from paid_client import ApClient

# Initialize the client
client = ApClient("your-api-key")

# Record usage events
client.record_usage(
    "your-agent-id",
    "customer-id",
    "event-name",
    {"your": "data"}
)

# Events are automatically flushed every 30 seconds
# or when the buffer reaches 100 events
# To manually flush:
client.flush()
```