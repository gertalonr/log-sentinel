from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.orm import Session

from app.api import deps
from app.db.mongo import get_mongo_db
from app.models.project import Project
from app.models.user import User
from app.schemas.log import LogCreate, LogResponse

router = APIRouter()

async def get_project_by_api_key(
    x_api_key: str = Header(...), db: Session = Depends(deps.get_db)
) -> Project:
    project = db.query(Project).filter(Project.api_key == x_api_key).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )
    return project

@router.post("/ingest", response_model=LogResponse)
async def ingest_log(
    log_in: LogCreate,
    project: Project = Depends(get_project_by_api_key),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> Any:
    """
    Ingest a new log entry.
    """
    log_dict = log_in.dict()
    log_dict["project_id"] = str(project.id)
    log_dict["received_at"] = datetime.utcnow()
    
    result = await mongo_db["logs"].insert_one(log_dict)
    
    log_dict["id"] = str(result.inserted_id)
    return log_dict

@router.get("/", response_model=List[LogResponse])
async def read_logs(
    project_id: UUID, 
    current_user: User = Depends(deps.get_current_user),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve logs for a specific project.
    """
    # Verify project ownership
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    cursor = mongo_db["logs"].find({"project_id": str(project_id)}).skip(skip).limit(limit).sort("received_at", -1)
    logs = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        logs.append(doc)
    
    return logs
