from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.orm import Session

from app.api import deps
from app.db.mongo import get_mongo_db
from app.models.project import Project
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai import analyze_logs

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_logs(
    chat_in: ChatRequest,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
) -> Any:
    """
    Analyze logs using AI.
    """
    # 1. Validate Project Ownership
    project = db.query(Project).filter(
        Project.id == chat_in.project_id, 
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")

    # 2. Fetch logs from MongoDB (Last 50)
    cursor = mongo_db["logs"].find(
        {"project_id": str(chat_in.project_id)}
    ).sort("received_at", -1).limit(50)
    
    logs = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"]) # Serialize ID
        logs.append(doc)

    if not logs:
        return ChatResponse(response="No logs found for this project.")

    # 3. Analyze with AI
    ai_response = await analyze_logs(chat_in.question, logs)
    
    return ChatResponse(response=ai_response)
