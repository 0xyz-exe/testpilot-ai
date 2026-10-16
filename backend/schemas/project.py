from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    allowed_urls: List[str]

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    allowed_urls: Optional[List[str]] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    allowed_urls: List[str]
    test_count: Optional[int] = 0
    pass_rate: Optional[float] = None
    last_run_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
