from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from projectdavid_common.schemas.vectors import VectorStoreRead


# --- AssistantCreate ---
class AssistantCreate(BaseModel):
    id: Optional[str] = Field(
        None,
        description="Unique identifier for the assistant. Optional on creation.",
    )
    name: str = Field(..., description="Name of the assistant")
    description: str = Field("", description="A brief description of the assistant")
    model: str = Field(..., description="Model used by the assistant")
    instructions: str = Field(
        "", description="Special instructions or guidelines for the assistant"
    )
    tools: Optional[List[dict]] = Field(
        None,
        description="A list of tools available to the assistant, each defined as a dictionary",
    )
    platform_tools: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Optional array of inline tool specifications for the assistant, e.g. [{'type': 'file_search', 'vector_store_ids': ['...']}]",
    )
    meta_data: Optional[dict] = Field(None, description="Additional metadata for the assistant")
    top_p: float = Field(1.0, description="Top-p sampling parameter for text generation")
    temperature: float = Field(1.0, description="Temperature parameter for text generation")
    response_format: str = Field("auto", description="Format of the assistant's response")

    webhook_url: Optional[HttpUrl] = Field(
        None,
        description="Optional URL endpoint to send 'run.action_required' webhook events to.",
        examples=["https://myapp.com/webhooks/projectdavid/actions"],
    )
    webhook_secret: Optional[str] = Field(
        None,
        min_length=16,
        description="Optional secret used to sign outgoing 'run.action_required' webhooks. Min 16 chars.",
        examples=["whsec_MySecureS3cr3tValueF0rHMAC"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Webhook Enabled Assistant",
                "description": "An assistant configured for webhooks",
                "model": "gpt-4-turbo",
                "instructions": "Use tools when needed and await webhook callback.",
                "tools": [{"name": "get_flight_times"}],
                "platform_tools": [{"type": "file_search", "vector_store_ids": ["vs_demo_store"]}],
                "meta_data": {"project": "webhook-test"},
                "top_p": 0.9,
                "temperature": 0.7,
                "response_format": "auto",
                "webhook_url": "https://api.example.com/my-webhook-receiver",
                "webhook_secret": "whsec_ReplaceWithARealSecureSecretKey123",
            }
        }
    )


# --- AssistantRead ---
class AssistantRead(BaseModel):
    id: str = Field(..., description="Unique identifier for the assistant")
    user_id: Optional[str] = Field(
        None, description="Identifier for the user associated with the assistant"
    )
    object: str = Field(..., description="Object type")
    created_at: int = Field(..., description="Timestamp when the assistant was created")
    name: str = Field(..., description="Name of the assistant")
    description: Optional[str] = Field(None, description="Description of the assistant")
    model: str = Field(..., description="Model used by the assistant")
    instructions: Optional[str] = Field(None, description="Instructions provided to the assistant")
    tools: Optional[List[dict]] = Field(
        None, description="List of tool definitions associated with the assistant"
    )
    platform_tools: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Inline platform tool specifications attached directly to the assistant",
    )
    meta_data: Optional[Dict[str, Any]] = Field(
        None, description="Additional metadata for the assistant"
    )
    top_p: float = Field(..., description="Top-p sampling parameter")
    temperature: float = Field(..., description="Temperature parameter")
    response_format: str = Field(..., description="Response format")
    vector_stores: Optional[List[VectorStoreRead]] = Field(
        default_factory=list, description="List of associated vector stores"
    )

    webhook_url: Optional[HttpUrl] = Field(
        None, description="Configured URL endpoint for 'run.action_required' webhooks (if any)."
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "asst_abc123",
                "user_id": "user_xyz",
                "object": "assistant",
                "created_at": 1710000000,
                "name": "Webhook Enabled Assistant",
                "description": "Assistant configured for webhooks",
                "model": "gpt-4-turbo",
                "instructions": "Use tools when needed and await webhook callback.",
                "tools": [{"name": "get_flight_times"}],
                "platform_tools": [{"type": "file_search", "vector_store_ids": ["vs_demo_store"]}],
                "meta_data": {"department": "automation"},
                "top_p": 1.0,
                "temperature": 0.7,
                "response_format": "auto",
                "vector_stores": [],
                "webhook_url": "https://api.example.com/my-webhook-receiver",
            }
        },
    )


# --- AssistantUpdate ---
class AssistantUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Updated name for the assistant")
    description: Optional[str] = Field(None, description="Updated description for the assistant")
    model: Optional[str] = Field(None, description="Updated model name")
    instructions: Optional[str] = Field(None, description="Updated instructions for the assistant")
    tools: Optional[List[Any]] = Field(None, description="Updated list of tools for the assistant")
    platform_tools: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Updated inline platform tool specifications for the assistant",
    )
    meta_data: Optional[Dict[str, Any]] = Field(
        None, description="Updated metadata for the assistant"
    )
    top_p: Optional[float] = Field(None, description="Updated top-p parameter")
    temperature: Optional[float] = Field(None, description="Updated temperature parameter")
    response_format: Optional[str] = Field(None, description="Updated response format")

    webhook_url: Optional[HttpUrl] = Field(
        None,
        description="Updated URL endpoint for 'run.action_required' webhooks. Set to null to remove.",
        examples=["https://myapp.com/webhooks/new_endpoint", None],
    )
    webhook_secret: Optional[str] = Field(
        None,
        min_length=16,
        description="Updated secret for signing webhooks. Min 16 chars. Provide only if changing.",
        examples=["whsec_AnotherSecureSecretKeyABC"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Assistant Name",
                "instructions": "New instructions here.",
                "platform_tools": [{"type": "calculator"}],
                "webhook_url": "https://api.example.com/my-new-webhook-endpoint",
            }
        }
    )
