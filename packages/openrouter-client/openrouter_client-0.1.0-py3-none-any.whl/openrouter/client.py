import json
import httpx
from fastapi import FastAPI
from typing import Dict, Any, AsyncGenerator
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from openrouter.core.config import settings
from openrouter.models.request import ChatCompletionRequest
from openrouter.models.response import OpenRouterResponse

api_router = APIRouter(
    prefix=settings.OPENROUTER_API_PREFIX,
    tags=["OpenRouter"],
    responses={
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"}
    },
)

def create_app() -> FastAPI:
    """
    Create a standalone FastAPI application with the OpenRouter API router mounted.

    Returns:
        FastAPI: A FastAPI application instance with the OpenRouter API router configured

    Example:
        ```python
        from openrouter import create_app

        app = create_app()
        # Run with uvicorn
        # uvicorn main:app --reload
        ```
    """
    app = FastAPI(
        title="OpenRouter API Client",
        description="A FastAPI application for the OpenRouter API",
        version=__import__("openrouter").__version__,
    )

    app.include_router(api_router)

    @app.get("/")
    def root():
        return {
            "message": "OpenRouter API Client using FastAPI",
            "docs_url": "/docs",
            "openapi_url": "/openapi.json"
        }

    return app


def get_headers() -> Dict[str, str]:
    """Get headers for OpenRouter API requests"""
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        'HTTP-Referer': settings.OPENROUTER_HEADER_REFERER,
        'X-Title': settings.OPENROUTER_HEADER_TITLE,
    }


def parse_openrouter_response(data: Dict[str, Any]) -> OpenRouterResponse:
    """
    Parse an OpenRouter API response into the appropriate response type based on the 'object' field

    Args:
        data: The raw response data from the OpenRouter API

    Returns:
        The parsed response object of the appropriate type
    """
    print(f"Parsing OpenRouter response with object type: {data.get('object')}. Response data: {data}")
    object_type = data.get("object")

    try:
        # Make sure only valid object types are processed
        if object_type == "chat.completion.chunk" or object_type == "chat.completion":
            return OpenRouterResponse(**data)
    except ValueError as e:
        # Fail if the object type is not recognized
        raise HTTPException(
            status_code=422,
            detail=f"Unknown response object with param 'object': {object_type} in OpenRouter API response."
        )


async def stream_openrouter_response(response: httpx.Response) -> AsyncGenerator[str, Any]:
    async for line in response.aiter_lines():
        decoded_line = line.strip()
        if not decoded_line:
            continue

        # Handle SSE format (data: prefix)
        if decoded_line.startswith('data: '):
            decoded_line = decoded_line[6:]  # Remove 'data: ' prefix
            try:
                # End of stream marker
                if decoded_line =="[DONE]":
                    yield f"data: {decoded_line}"
                    break
                else:
                    data = json.loads(decoded_line)
                    # validate the response with pydantic model
                    response_obj = OpenRouterResponse(**data)
                    yield f"data: {json.dumps(response_obj.model_dump(exclude_none=True))}\n\n"
            except json.JSONDecodeError:
                # Skip malformed JSON
                print(f"Skipping malformed JSON: {decoded_line}")
                continue
            except Exception as e:
                # Log error but continue streaming
                print(f"Error processing stream chunk: {str(e)}")
                continue


@api_router.post("/chat", response_model=OpenRouterResponse)
async def create_chat_completion(request: ChatCompletionRequest):
    """
    Create a chat completion using OpenRouter API

    This endpoint proxies requests to OpenRouter and handles both streaming and non-streaming responses.
    """
    # Build the endpoint URL
    endpoint_url = f"{settings.OPENROUTER_URL}/chat/completions"

    # Get request payload and add HTTP metadata if not already present
    payload = request.model_dump(exclude_none=True)

    # Determine if this is a streaming request
    is_streaming = payload.get("stream", False)

    try:
        # Handle streaming response
        if is_streaming:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint_url,
                    headers=get_headers(),
                    json=payload,
                    timeout=300  # 5 minute timeout
                )

                if response.status_code != 200:
                    error_text = response.text
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"OpenRouter API error: {error_text}"
                    )

                # Return streaming response
                return StreamingResponse(
                    stream_openrouter_response(response),
                    media_type="text/event-stream"
                )

        # Handle regular (non-streaming) response
        else:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    endpoint_url,
                    headers=get_headers(),
                    json=payload,
                    timeout=120  # 2 minute timeout
                )

                response_data = response.json()

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"OpenRouter API error: {response_data}"
                    )

                # Parse and validate the response
                validated_response = parse_openrouter_response(response_data)
                return validated_response

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error communicating with OpenRouter API: {str(e)}"
        )
    except Exception as e:
        # Catch-all exception handler
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
