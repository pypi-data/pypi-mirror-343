# Unit tests for OpenRouter client
# These tests use mocks to avoid making actual API calls
# Make sure pytest is installed: pip install pytest pytest-asyncio
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from httpx import Response

from openrouter import create_app
from openrouter.client import get_headers
from openrouter.models.request import ChatCompletionRequest
from openrouter.core.config import settings


@pytest.fixture
def test_model_name():
    """Get the model name"""
    return "meta-llama/llama-3.2-1b-instruct:free"


# Test fixtures
@pytest.fixture
def mock_completion_response(test_model_name):
    """Mock response data for a chat completion"""
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": test_model_name,
        "choices": [{
            "message": {
                "role": "assistant",
                "content": "Hello, how can I help you today?"
            },
            "finish_reason": "stop",
            "native_finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 5,
            "completion_tokens": 10,
            "total_tokens": 15
        },
        "model_owner": "Meta"
    }


@pytest.fixture
def mock_streaming_responses(test_model_name):
    """Mock streaming response chunks"""
    return [
        f"data: {{\"id\":\"chatcmpl-123\",\"object\":\"chat.completion.chunk\",\"created\":1677652288,\"model\":\"{test_model_name}\",\"choices\":[{{\"delta\":{{\"role\":\"assistant\"}},\"finish_reason\":null}}]}}\n\n",
        f"data: {{\"id\":\"chatcmpl-123\",\"object\":\"chat.completion.chunk\",\"created\":1677652288,\"model\":\"{test_model_name}\",\"choices\":[{{\"delta\":{{\"content\":\"Hello\"}},\"finish_reason\":null}}]}}\n\n",
        f"data: {{\"id\":\"chatcmpl-123\",\"object\":\"chat.completion.chunk\",\"created\":1677652288,\"model\":\"{test_model_name}\",\"choices\":[{{\"delta\":{{\"content\":\", how can I help you today?\"}},\"finish_reason\":\"stop\"}}],\"usage\":{{\"prompt_tokens\":5,\"completion_tokens\":10,\"total_tokens\":15}}}}\n\n",
        'data: [DONE]\n\n'
    ]


@pytest.fixture
def app():
    """Create a test FastAPI app"""
    return create_app()


@pytest.fixture
def client(app):
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_request(test_model_name):
    """Create a sample chat completion request"""
    return ChatCompletionRequest(
        messages=[{"role": "user", "content": "Hello"}],
        model=test_model_name
    )


# Tests for client utility functions
def test_get_headers():
    """Test the get_headers function"""
    # Set a test API key
    original_key = settings.OPENROUTER_API_KEY
    settings.OPENROUTER_API_KEY = "test_key"

    try:
        headers = get_headers()
        assert headers["Content-Type"] == "application/json"
        assert headers["Authorization"] == "Bearer test_key"
    finally:
        # Restore the original API key
        settings.OPENROUTER_API_KEY = original_key


# Tests for standalone app
def test_standalone_app(app):
    """Test that the standalone app is created correctly"""
    assert app is not None
    # Check that our router was included
    routes = [route for route in app.routes if route.path.startswith(settings.OPENROUTER_API_PREFIX)]
    assert len(routes) > 0


def test_root_endpoint(client):
    """Test the root endpoint of the standalone app"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "OpenRouter API Client using FastAPI"


# Tests for API endpoints
def test_chat_endpoint(client, mock_completion_response, test_model_name):
    """Test the chat completion API endpoint"""
    # Mock the AsyncClient post method
    with patch("httpx.AsyncClient.post") as mock_post:
        # Configure the mock
        mock_response = AsyncMock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = mock_completion_response
        mock_post.return_value = mock_response

        # Make a request to the endpoint
        response = client.post(
            f"{settings.OPENROUTER_API_PREFIX}/chat",
            json={
                "messages": [{"role": "user", "content": "Hello"}],
                "model": test_model_name
            }
        )

        # Check the response
        assert response.status_code == 200
        data = response.json()
        assert data["model"] == test_model_name
        assert data["choices"][0]["message"]["content"] == "Hello, how can I help you today?"


def test_streaming_chat_endpoint(client, mock_streaming_responses):
    """Test the streaming chat completion API endpoint"""
    # Mock the AsyncClient post and Response.aiter_lines methods
    with patch("httpx.AsyncClient.post") as mock_post:
        # Create a mock response that will be used for streaming
        mock_response = MagicMock()
        mock_response.status_code = 200

        # Configure the aiter_lines method to yield our test data
        async def mock_aiter_lines():
            for line in mock_streaming_responses:
                yield line

        mock_response.aiter_lines = mock_aiter_lines
        mock_post.return_value = mock_response

        # Make a streaming request to the endpoint
        with client.stream(
            "POST",
            f"{settings.OPENROUTER_API_PREFIX}/chat",
            json={
                "messages": [{"role": "user", "content": "Hello"}],
                "model": "openai/gpt-4-turbo",
                "stream": True
            }
        ) as response:
            # Check response is streaming properly
            assert response.status_code == 200
            assert response.headers["content-type"].startswith("text/event-stream")

            # Collect all streaming chunks
            chunks = []
            for chunk in response.iter_lines():
                if chunk:
                    chunks.append(chunk)

            # Verify we got the expected number of chunks
            assert len(chunks) > 0
            # Check for the DONE marker
            assert any("[DONE]" in chunk for chunk in chunks)
