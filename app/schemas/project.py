from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: UUID
    api_key: str
    owner_id: int

    class Config:
        from_attributes = True
