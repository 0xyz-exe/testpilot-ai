from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .config import settings
from .database import get_db, init_db
from .models import User
from .schemas.auth import UserRegister, UserLogin, UserResponse
from .services.auth import create_user, authenticate_user
from .routes.projects import router as projects_router

app = FastAPI(title="TestPilot AI", version="1.0.0")

app.include_router(projects_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Auth endpoints
@app.post("/api/v1/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if user exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = create_user(db, user_data)
    return user

@app.post("/api/v1/auth/login", response_model=dict)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # For MVP: return user data (session management added later)
    return {"user": {"id": user.id, "email": user.email}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
