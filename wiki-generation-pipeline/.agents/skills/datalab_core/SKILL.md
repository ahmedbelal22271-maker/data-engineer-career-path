---
name: Datalab Core SDK
description: Base installation, authentication, and error handling for the Datalab SDK. Required foundation for all other datalab skills.
---

# Datalab Core SDK

## 1. Installation: The Package Trap
> ⚠️ **CRITICAL: Do NOT run `pip install datalab`.** This points to an ancient, abandoned package.
**Correct command:**
`pip install datalab-python-sdk`

## 2. Authentication & Client Initialization
Note the difference: the pip package name uses **hyphens** (`datalab-python-sdk`) but the Python module uses an **underscore** (`datalab_sdk`).

```python
import os
from datalab_sdk import DatalabClient, AsyncDatalabClient

# Sync Client (Uses DATALAB_API_KEY env var by default)
client = DatalabClient()

# Async Client (for high-throughput applications)
async def main():
    async with AsyncDatalabClient() as client:
        pass
```

## 3. Error Handling
The SDK raises specific exceptions that should be caught:

```python
from datalab_sdk.exceptions import (
    DatalabAPIError,         # API returned an error response
    DatalabTimeoutError,     # Request exceeded timeout
    DatalabFileError,        # File not found or cannot be read
    DatalabValidationError,  # Invalid parameters provided
)

try:
    pass # execute datalab method
except DatalabAPIError as e:
    print(f"API error {e.status_code}: {e.response_data}")
```

## 4. Full Documentation Reference
For complete documentation on Quickstart, Welcome guides, and exhaustive API parameters, read the raw markdown files located in the `references/` subdirectory of this skill.
