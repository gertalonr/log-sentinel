```python
from typing import Optional
from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr]# --- INJECT LIFESPAN --- is_active: Optional[bool] = True

# Properties to receive via API on creation
class UserCreate(UserBase):
  # --- NEW: LIFESPAN MANAGER ---password: str

# Properties to return via API
class User(UserBase):
    print("🚀 LogSentinel: Configuring MongoDB indices...")e

    class Config:
    # 🟢 STARTUP: Create indicesbutes = True

# Properties stored in DB
class UserInDB(UserBase):
    hashed_password: str
```
