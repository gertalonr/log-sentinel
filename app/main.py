from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1.endpoints import auth, users, projects, logs, chat
from app.db.mongo import get_mongo_db

# --- NEW: LIFESPAN MANAGER ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🟢 STARTUP: Create indices
    print("🚀 LogSentinel: Configuring MongoDB indices...")
    try:
        # 👇👇👇 ERROR FIX: Added 'await'
        db = await get_mongo_db() 
        
        # Now 'db' is the actual database, not a coroutine
        await db["logs"].create_index([("project_id", 1), ("timestamp", -1)])
        print("✅ Indices created successfully.")
    except Exception as e:
        # Print complete error for debugging
        print(f"⚠️ Alert: Could not create indices: {e}")
    
    yield
    pass

# --- INJECT LIFESPAN ---
app = FastAPI(
    title="Log Sentinel API",
    lifespan=lifespan  # <--- CRITICAL! Connect the manager
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(logs.router, prefix="/api/v1/logs", tags=["logs"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Mount Static Files (Frontend)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")