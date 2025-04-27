from typing import List, Optional, Union, Literal
from fastapi import HTTPException
from pydantic import BaseModel, Field, model_validator

from .helpers import ResponseUsage, ResponseChoiceModel

class OpenRouterResponse(BaseModel):
    """Chat response model"""
    id: str = Field(..., description="Unique identifier for the completion")
    choices: List[ResponseChoiceModel] = Field(..., description="List of completion choices")
    created: int = Field(..., description="Unix timestamp of when the completion was created")
    model: str = Field(..., description="Model used for completion")
    object: Union[Literal["chat.completion"], Literal["chat.completion.chunk"]] = Field(..., description="Type of response object")
    system_fingerprint: Optional[str] = Field(
        None,
        description="System fingerprint used for content moderation (only present if the provider supports it)"
    )
    usage: Optional[ResponseUsage] = Field(None, description="Token usage statistics")
    model_owner: Optional[str] = Field(None, description="The owner/provider of the model")

    @model_validator(mode='before')
    @classmethod
    def check_type(cls, values):
        if not isinstance(values, dict):
            raise HTTPException(
                status_code=422,
                detail=f"Response did not contain dictionary data in OpenRouter API response. Response: {values}"
            )
        # Make sure to check if 'choices' is present in the values
        if 'choices' not in values:
            raise HTTPException(
                status_code=422,
                detail=f"Missing 'choices' field in OpenRouter API response. Response: {values}"
            )

        # We have to inject the type of choices returned specifically
        # since the discriminators from OpenRouter API are fields and not
        # values in the response data
        object_type = values.get('object')
        choice = values.get('choices')[0]

        if object_type == "chat.completion.chunk":
            if 'text' in choice and 'delta' not in choice:
                values['choices'][0]['delta'] = {'content': choice['text']}
            values['choices'][0]['type'] = 'streaming'
        elif object_type == "chat.completion":
            if 'text' in choice:
                values['choices'][0]['type'] = 'non_chat'
            elif 'message' in choice:
                values['choices'][0]['type'] = 'non_streaming'
            else:
                raise ValueError(f"Unknown choice type: {choice} in OpenRouter API response.")
        else:
            raise ValueError(f"Unknown response object with param 'object': {object_type} in OpenRouter API response.")
        return values
