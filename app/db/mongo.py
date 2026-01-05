from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db = MongoDB()

async def get_mongo_db():
    if db.client is None:
        db.client = AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
        db.db = db.client[settings.MONGO_DB]
    return db.db

def close_mongo_connection():
    if db.client:
        db.client.close()
