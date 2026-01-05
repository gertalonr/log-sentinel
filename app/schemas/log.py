from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import BaseModel, Field

class LogCreate(BaseModel):
    level: str
    message: str
    service_name: str
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    extra: Optional[Dict[str, Any]] = None

class LogResponse(LogCreate):
    id: str = Field(..., description="MongoDB Object ID")
    project_id: UUID
    received_at: datetime
