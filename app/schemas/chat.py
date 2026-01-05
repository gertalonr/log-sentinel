from uuid import UUID
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    project_id: UUID

class ChatResponse(BaseModel):
    response: str
