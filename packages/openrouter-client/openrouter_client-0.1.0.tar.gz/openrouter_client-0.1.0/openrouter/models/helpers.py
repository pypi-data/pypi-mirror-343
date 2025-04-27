from typing import Dict, List, Optional, Union, Literal, Any
from typing_extensions import Annotated

from pydantic import BaseModel, Field, field_validator
import logging

logger = logging.getLogger(__name__)

# Common utility models for both requests and responses

class ErrorResponse(BaseModel):
    """Error response from the API"""
    code: int = Field(..., description="Error code. See 'Error Handling' section")
    message: str = Field(..., description="Error message")
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Contains additional error information such as provider details, the raw error message, etc."
    )


# Content and message-related models

class TextContentPart(BaseModel):
    """Text content part for messages"""
    type: Literal["text"] = "text"
    text: str


class ImageUrl(BaseModel):
    """Image URL specification"""
    url: str  # URL or base64 encoded image data
    detail: Optional[str] = "auto"


class ImageContentPart(BaseModel):
    """Image content part for messages"""
    type: Literal["image_url"] = "image_url"
    image_url: ImageUrl


ContentPart = Annotated[Union[TextContentPart, ImageContentPart], Field(discriminator="type", description="Content part type")]


# Tool and function-related models

class FunctionDescription(BaseModel):
    """Description of a function for function calling"""
    name: str
    parameters: Dict[str, Any]  # JSON Schema object
    description: Optional[str] = None


class Tool(BaseModel):
    """Tool definition for tool calling"""
    type: Literal["function"] = "function"
    function: FunctionDescription


class FunctionToolChoice(BaseModel):
    """Specific function choice for tool_choice"""
    type: Literal["function"] = "function"
    function: Dict[str, str] = Field(..., examples=[{"name": "exampleFunction"}])


class NoneToolChoice(BaseModel):
    type: Literal["none"] = "none"


class AutoToolChoice(BaseModel):
    type: Literal["auto"] = "auto"


ToolChoice = Annotated[
    Union[NoneToolChoice, AutoToolChoice, FunctionToolChoice],
    Field(discriminator="type")
]


class FunctionCall(BaseModel):
    """Function call details"""
    name: str = Field(..., description="Name of the function to call")
    arguments: str = Field(..., description="Arguments to pass to the function, as a JSON string")


class ToolCall(BaseModel):
    """Tool call in response"""
    id: str = Field(..., description="Unique identifier for the tool call")
    type: Literal["function"] = "function"
    function: FunctionCall = Field(..., description="Function call details")


# Message-related models

class BaseMessage(BaseModel):
    """Base message model with common fields"""
    name: Optional[str] = None


class UserAssistantSystemMessage(BaseMessage):
    """Message from user, assistant, or system"""
    role: Literal["user", "assistant", "system"]
    content: Annotated[Union[str, List[ContentPart]], Field(description="Content of the message")]


class ToolMessage(BaseMessage):
    """Message from a tool"""
    role: Annotated[Literal["tool"], Field(description="Role of the message")] = "tool"
    content: str
    tool_call_id: str


Message = Annotated[Union[UserAssistantSystemMessage, ToolMessage], Field(discriminator="role", description="Allowed values: 'user', 'assistant', 'system', 'tool'")]


class ResponseMessage(BaseModel):
    """Message in a non-streaming response"""
    role: str = Field(..., description="Role of the message author (e.g., 'assistant')")
    content: Optional[str] = Field(None, description="Content of the message")
    tool_calls: Optional[List[ToolCall]] = Field(None, description="List of tool calls if the model called tools")


class Delta(BaseModel):
    """Delta in a streaming response"""
    content: Optional[str] = Field(None, description="Content delta for this chunk")
    role: Optional[str] = Field(None, description="Role of the message author (only in first chunk)")
    tool_calls: Optional[List[ToolCall]] = Field(None, description="List of tool calls if the model called tools")


# Other utility models

class PredictionContent(BaseModel):
    """Content for prediction field"""
    type: Literal["content"] = "content"
    content: str


class ProviderSettings(BaseModel):
    """Provider preferences for routing"""
    order: Annotated[Optional[List[str]], Field(default=None, description="List of provider names to try in order (e.g. ['Anthropic', 'OpenAI'])")]
    allow_fallbacks: Annotated[bool, Field(default=True, description="Whether to allow backup providers when the primary is unavailable")]
    require_parameters: Annotated[bool, Field(default=False, description="Only use providers that support all parameters in your request")]
    data_collection: Annotated[Literal["allow", "deny"], Field(default="allow", description="Control whether to use providers that may store data")]
    ignore: Annotated[Optional[List[str]], Field(default=None, description="List of provider names to skip for this request")]
    quantizations: Annotated[Optional[List[str]], Field(default=None, description="List of quantization levels to filter by (e.g. ['int4', 'int8'])")]
    sort: Annotated[Optional[Literal["price", "throughput"]], Field(default=None, description='Sort providers by price or throughput (e.g. "price" or "throughput")')]


class Reasoning(BaseModel):
    """Configuration for model reasoning/thinking tokens"""
    effort: Annotated[Optional[Literal["high", "medium", "low"]], Field(default=None, description="OpenAI-style reasoning effort setting")]
    max_tokens: Annotated[Optional[int], Field(default=None, description="Non-OpenAI-style reasoning effort setting. Cannot be used simultaneously with effort.")]
    exclude: Annotated[Optional[bool], Field(default=False, description="Whether to exclude reasoning from the response")]

    @field_validator("effort", "max_tokens")
    @classmethod
    def validate_effort_and_max_tokens(cls, values):
        if values.get("effort") is not None and values.get("max_tokens") is not None:
            raise ValueError("'effort' and 'max_tokens' cannot be used simultaneously")
        return values


class UsageConfig(BaseModel):
    """Configuration for usage information inclusion in the response"""
    include: Annotated[Optional[bool], Field(default=None, description="Whether to include usage information in the response")]


class ResponseUsage(BaseModel):
    """Token usage information"""
    prompt_tokens: int = Field(..., description="Number of tokens in the prompt, including images and tools if any")
    completion_tokens: int = Field(..., description="Number of tokens in the completion")
    total_tokens: int = Field(..., description="Total number of tokens used (prompt + completion)")


# Response choice models

class NonChatChoice(BaseModel):
    """Choice in a non-chat (completion) response"""
    type: Literal["non_chat"] = "non_chat"
    finish_reason: Optional[str] = Field(None, description="The reason generation stopped")
    native_finish_reason: Optional[str] = Field(None, description="Native finish reason from the provider")
    text: str = Field(..., description="The generated text")
    error: Optional[ErrorResponse] = Field(None, description="Error information if request failed")


class NonStreamingChoice(BaseModel):
    """Choice in a non-streaming response"""
    type: Literal["non_streaming"] = "non_streaming"
    finish_reason: Optional[str] = Field(None, description="The reason generation stopped")
    native_finish_reason: Optional[str] = Field(None, description="Native finish reason from the provider")
    message: ResponseMessage = Field(..., description="The generated message")
    error: Optional[ErrorResponse] = Field(None, description="Error information if request failed")


class StreamingChoice(BaseModel):
    """Choice in a streaming response"""
    type: Literal["streaming"] = "streaming"
    finish_reason: Optional[str] = Field(None, description="The reason generation stopped (only in last chunk)")
    native_finish_reason: Optional[str] = Field(None, description="Native finish reason from the provider")
    delta: Delta = Field(..., description="The content delta for this streaming response")
    error: Optional[ErrorResponse] = Field(None, description="Error information if request failed")

ResponseChoiceModel = Annotated[
    Union[NonChatChoice, NonStreamingChoice, StreamingChoice],
    Field(discriminator="type", description="Allowed values: 'non_chat', 'non_streaming', 'streaming'")
]