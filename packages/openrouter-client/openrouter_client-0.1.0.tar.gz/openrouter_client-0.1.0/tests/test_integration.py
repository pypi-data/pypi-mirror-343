import pytest
import warnings

from openrouter.client import create_chat_completion
from openrouter.models.request import ChatCompletionRequest
from openrouter.core.config import settings
from openrouter.models.response import OpenRouterResponse

# Skip all tests in this module if integration testing is disabled
pytestmark = pytest.mark.skipif(
    not settings.OPENROUTER_INTEGRATION_TESTS,
    reason="Integration tests are disabled. Set OPENROUTER_INTEGRATION_TESTS=True to enable."
)


@pytest.fixture
def test_model_name():
    """Get the model name"""
    return settings.OPENROUTER_API_TEST_MODEL


@pytest.fixture
def test_prompt():
    """Get a simple test prompt"""
    return "Say hello in exactly 5 words."


@pytest.fixture(scope="module")
def use_env_api_key():
    """Check if API key is available for integration tests.

    This fixture validates that a proper API key is configured and skips
    tests if no valid key is found.
    """
    if not settings.OPENROUTER_API_KEY or settings.OPENROUTER_API_KEY == "your_openrouter_api_key":
        warnings.warn("No valid API key found. Integration tests will be skipped.")
        pytest.skip("No valid API key found")
    return settings.OPENROUTER_API_KEY


@pytest.mark.asyncio
async def test_chat_completion(use_env_api_key, test_model_name, test_prompt):
    """
    Integration test: Make a real API call to OpenRouter.

    This test actually calls the OpenRouter API with a simple request.
    It requires a valid API key set in your environment.
    """
    # Create a simple request
    request = ChatCompletionRequest(
        messages=[{"role": "user", "content": test_prompt}],
        model=test_model_name,  # Using a free model
        max_tokens=len(test_prompt) + 30,  # Keep response short
        temperature=0  # Make response deterministic
    )

    # Call the actual function - this makes a real API request
    response = await create_chat_completion(request)

    # Verify we got a proper response
    assert isinstance(response, OpenRouterResponse)
    assert response.choices[0].message.content is not None
    assert len(response.choices[0].message.content.split()) <= 10  # Allow some flexibility

    # Check for reasonable usage stats
    assert response.usage.prompt_tokens > 0
    assert response.usage.completion_tokens > 0
    assert response.usage.total_tokens > 0

    print(f"Actual API response: {response.choices[0].message.content}")
    print(f"Usage stats: {response.usage}")


@pytest.mark.asyncio
async def test_streaming_completion(use_env_api_key, test_prompt):
    """
    Integration test: Make a real streaming API call to OpenRouter.

    This test calls the OpenRouter API with streaming enabled and collects chunks.
    """
    from fastapi.responses import StreamingResponse
    import json

    # Create a streaming request
    request = ChatCompletionRequest(
        messages=[{"role": "user", "content": test_prompt}],
        model=settings.OPENROUTER_API_TEST_MODEL,  # Using a free model
        stream=True,
        max_tokens=len(test_prompt) + 30,  # Keep response short
        temperature=0
    )

    # Call the function - this triggers a real API call
    response = await create_chat_completion(request)

    # Verify we got a streaming response
    assert isinstance(response, StreamingResponse)
    assert response.media_type
    assert response.media_type.startswith("text/event-stream")

    # Collect and verify chunks
    chunks = []
    async for chunk in response.body_iterator:
        if chunk is str:
            print(chunk.__dict__)
            chunk.append(chunk)
        elif chunk is bytes:
            chunk = chunk.decode("utf-8")
            chunk.append(chunk)
        elif chunk is None:
            continue
        chunks.append(chunk)

    # Check that we got at least some chunks
    assert len(chunks) > 0
    # Check for the DONE marker
    assert any("[DONE]" in chunk for chunk in chunks)

    # Parse the chunks to extract content
    content = ""
    for chunk in chunks:
        if "data: " in chunk and "[DONE]" not in chunk:
            try:
                data = json.loads(chunk.replace("data: ", ""))
                if "choices" in data and data["choices"][0].get("delta", {}).get("content"):
                    content += data["choices"][0]["delta"]["content"]
            except:
                pass

    print(f"Streaming content: {content}")
    # Basic verification of content
    assert len(content) > 0
