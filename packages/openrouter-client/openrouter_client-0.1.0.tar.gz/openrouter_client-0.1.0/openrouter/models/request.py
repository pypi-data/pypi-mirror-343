from typing import Dict, List, Optional, Union, Literal, Any
from typing_extensions import Annotated
from pydantic import BaseModel, Field, field_validator

from .helpers import (
    Message, Tool, ToolChoice, PredictionContent,
    ProviderSettings, Reasoning, UsageConfig
)

class OpenRouterRequestModel(BaseModel):
    """Base model for OpenRouter API requests"""
    pass


class ChatCompletionRequest(BaseModel):
    """Request model for OpenRouter chat completions API"""
    # Core parameters - either messages or prompt is required
    messages: Annotated[Optional[List[Message]], Field(None, min_length=1, description="The messages to use.")]
    prompt: Annotated[Optional[str], Field(None, min_length=1, description="The prompt to use.")]

    # Model specification
    model: Annotated[Optional[str], Field(None, min_length=1, description="The model ID to use. If unspecified, the user's default is used.")]
    '''The model ID to use. If unspecified, the user's default is used.'''

    # See "Model Routing" section: openrouter.ai/docs/model-routing
    models: Annotated[Optional[List[str]], Field(None, description="Alternate list of models for routing overrides.")]
    route: Annotated[Optional[Literal["fallback"]], Field(None, description="Fallback routing override.")]

    # See "Provider Routing" section: openrouter.ai/docs/provider-routing
    provider: Annotated[Optional[ProviderSettings], Field(None, description="Preferences for provider routing.")]

    # Reasoning configuration
    reasoning: Annotated[Optional[Reasoning], Field(None, description="Configuration for model reasoning/thinking tokens")]

    # Usage information configuration
    usage: Annotated[Optional[UsageConfig], Field(None, description="Whether to include usage information in the response")]

    # See "Prompt Transforms" section: openrouter.ai/docs/transforms
    transforms: Annotated[Optional[List[str]], Field(None, description="List of prompt transforms to apply (OpenRouter-only).")]

    # Response format
    response_format: Annotated[Optional[Dict[str, str]], Field(default=None, description="The response format to use.")]

    # Control parameters
    stop: Annotated[Optional[Union[str, List[str]]], Field(None, description="List of tokens to stop generation on.")]
    stream: Annotated[Optional[bool], Field(None, description="Whether to stream the response.")]
    stream_options: Annotated[Optional[Dict[str, bool]], Field(None, description="Options for streaming the response.", examples=[{"include_usage": True}])]

    # LLM Parameters
    max_tokens: Annotated[Optional[int], Field(None, ge=1)]
    temperature: Annotated[Optional[float], Field(None, ge=0, le=2)]

    # Advanced LLM parameters
    seed: Annotated[Optional[int], Field(None, description="Seed for deterministic outputs.")]
    top_p: Annotated[Optional[float], Field(None, gt=0, le=1, description="Range: (0, 1]")]
    top_k: Annotated[Optional[int], Field(None, ge=1, description="Range: [1, Infinity) Not available for OpenAI models")]
    frequency_penalty: Annotated[Optional[float], Field(None, ge=-2, le=2)]
    presence_penalty: Annotated[Optional[float], Field(None, ge=-2, le=2)]
    repetition_penalty: Annotated[Optional[float], Field(None, gt=0, le=2)]
    logit_bias: Annotated[Optional[Dict[int, float]], Field(None, description="Logit bias for tokens.")]
    top_logprobs: Annotated[Optional[int], Field(None, description="Number of top logprobs to return.")]
    min_p: Annotated[Optional[float], Field(None, ge=0, le=1)]
    top_a: Annotated[Optional[float], Field(None, ge=0, le=1)]

    # Tool calling
    tools: Annotated[Optional[List[Tool]], Field(None, description="List of tools to use.")]
    tool_choice: Annotated[Optional[ToolChoice], Field(None, description="Tool choice strategy.")]

    # Latency optimization
    prediction: Annotated[Optional[PredictionContent], Field(None, description="Prediction content.")]

    # HTTP metadata
    http_referer: Annotated[Optional[str], Field(None, description="URL of your website or application")]
    http_user_agent: Annotated[Optional[str], Field(None, description="HTTP User-Agent header from your end-user")]

    @field_validator("messages", "prompt", mode="before")
    @classmethod
    def validate_messages_and_prompt(cls, value, info):
        # Check that messages and prompt are not both specified
        field_name = info.field_name
        data = info.data

        if field_name == "messages" and value is not None and data.get("prompt") is not None:
            raise ValueError("'messages' and 'prompt' cannot be used simultaneously")
        elif field_name == "prompt" and value is not None and data.get("messages") is not None:
            raise ValueError("'messages' and 'prompt' cannot be used simultaneously")
        return value


    # Validation to ensure either messages or prompt is provided
    def model_post_init(self, __context: Any) -> None:
        if self.messages is None and self.prompt is None:
            raise ValueError("Either 'messages' or 'prompt' must be provided")
        if self.stream_options is not None and self.stream is None:
            raise ValueError("'stream_options' requires 'stream' to be True")
