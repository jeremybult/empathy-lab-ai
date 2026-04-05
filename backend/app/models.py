from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    client_id: Optional[str] = Field(default=None, min_length=1)
    persona_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1, max_length=4000)


class ResetRequest(BaseModel):
    client_id: Optional[str] = Field(default=None, min_length=1)
    persona_id: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    reply: str
    mode: str
    client_id: str
    persona_id: str


class ResetResponse(BaseModel):
    status: str
    client_id: str
    persona_id: str
