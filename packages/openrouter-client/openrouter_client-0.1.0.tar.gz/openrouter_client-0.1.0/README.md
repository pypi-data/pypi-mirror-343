# OpenRouter Client

A Python client library for the [OpenRouter API](https://openrouter.ai/) using FastAPI.

**Currently supported APIs:**
- Chat Completion - `/chat/completions` (streaming / non-streaming)

Most parameters that I could figure out from the cryptic API docs are defined and usable. *I have not tested every parameter.*

**More API support coming soon!**

## Requirements
- Python 3.8 or higher

## Installation

### From PyPI
To install into your project directly from PyPI via `pip`:

```bash
pip install openrouter-client
```

If you're using `uv`:

```bash
uv add openrouter-client
```

### Build from source
To build the project from source, clone the repo and then run (Requires `uv` to be installed - instructions [here](https://docs.astral.sh/uv/getting-started/installation/)):

```bash
uv sync
```

## Configuration
**Requires** the following environment variable to be set:

```bash
export OPENROUTER_API_KEY="<your_api_key>"
```

Optional env variables (with their current defaults):

```bash
export OPENROUTER_API_URL="https://openrouter.ai/api/v1"
export OPENROUTER_API_PREFIX="/ai/openrouter"
export OPENROUTER_INTEGRATION_TESTS=False
export OPENROUTER_API_TEST_MODEL=meta-llama/llama-3.2-1b-instruct:free
export OPENROUTER_HEADER_TITLE=OpenRouter-PyClient
export OPENROUTER_HEADER_REFERER="https://github.com/mrcodepanda/openrouter-client"
```
Preferably, put these in an `.env` or `.env.dev` file in project root.

The last two are added to the request headers automatically. These values are for app rankings on OpenRouter site. Free to change to your app and site, if you like.

## Usage

For using the api, here are various ways to setup (almost all parameters in [OpenRouter REST API](https://openrouter.ai/docs/api-reference/overview) are available)

### Option 1: Use as a standalone FastAPI app

```python
from openrouter import create_app

app = create_app()

# Run with uvicorn (assuming main.py is the name of the file)
# uvicorn main:app --reload
```

### Option 2: Add to an existing FastAPI app

```python
from fastapi import FastAPI
from openrouter import api_router

app = FastAPI()

# You can add dependencies and other options available for FastAPI Routers as well. For eg.
api_router.dependencies = [Depends(some_dependency)]

app.include_router(api_router)

# Now the OpenRouter endpoints are available at /ai/openrouter/*
# Optionally, you can customize the API prefix with OPENROUTER_API_PREFIX env variable
```

### Option 3: Use as a client library

```python
from openrouter.client import create_chat_completion
from openrouter.models.request import ChatCompletionRequest

# Example usage
request = ChatCompletionRequest(
    messages=[{"role": "user", "content": "Hello, how are you?"}],
    model="<model_name>"
)

response = await create_chat_completion(request)
```

## Testing

***Read [integration testing](#integration-testing) section before running tests***

To run the tests, install test dependencies:
```bash
# Using requirements file
pip install -r requirements-dev.txt
pytest

# Or using uv
uv sync --extra dev
pytest
```
### Integration Testing
The package includes both unit tests (with mocks) and integration tests (with real API calls).

To run integration tests:
1. Set your OpenRouter API key in the environment or .env file
2. Enable integration tests with an environment variable:
```bash
# Enable integration tests
export OPENROUTER_INTEGRATION_TESTS=True
```

3. **[OPTIONAL]** Set the OpenRouter API test model with an environment variable:
```bash
# Set the OpenRouter API test model
export OPENROUTER_API_TEST_MODEL="meta-llama/llama-3.2-1b-instruct:free"
```

4. Run tests
```bash
# Run all tests including integration tests
pytest

# Run only mock tests (no calls directly to OpenRouter API)
pytest tests/test_openrouter.py

# Run only integration tests
# Strict max tokens set to 5 to be safe
pytest tests/test_integration.py
```

*Integration tests make actual API calls to OpenRouter API. By default, the api uses `meta-llama/llama-3.2-1b-instruct:free` for faster tests with max 30 tokens for output. This model can be changed by setting the `OPENROUTER_API_TEST_MODEL` environment variable. Current free API call limits can be checked [here](https://openrouter.ai/docs/api-reference/limits#rate-limits-and-credits-remaining).*

## Issues & Improvements

If you find an issue, submit a PR or open an issue in the issues tab [here](https://github.com/mrcodepanda/openrouter-client/issues) and I will get back to you as soon as I can.

## Contribute

If you'd like to contribute, simply fork the repository, commit your changes to `master` branch (or branch off of it), and send a pull request. Make sure you add yourself to [AUTHORS](https://github.com/mrcodepanda/openrouter-client/blob/master/AUTHORS) in the pull request.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/mrcodepanda/openrouter-client/blob/master/LICENSE) file for details.

Copyright (C) 2025 Sudhanshu Aggarwal (@mrcodepanda)
