from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Project, User
from ..schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from ..security.url_validator import validate_allowed_urls
import json

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])

def get_current_user(db: Session = Depends(get_db)) -> User:
    # TODO: session/JWT auth
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

@router.get("", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    projects = db.query(Project).filter(Project.user_id == user.id).all()
    
    result = []
    for p in projects:
        result.append(ProjectResponse(
            id=p.id,
            name=p.name,
            allowed_urls=json.loads(p.allowed_urls),
            test_count=0,
            created_at=p.created_at
        ))
    return result

@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    validate_allowed_urls(project.allowed_urls)
    
    new_project = Project(
        user_id=user.id,
        name=project.name,
        allowed_urls=json.dumps(project.allowed_urls),
        settings=json.dumps({})
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return ProjectResponse(
        id=new_project.id,
        name=new_project.name,
        allowed_urls=json.loads(new_project.allowed_urls),
        test_count=0,
        created_at=new_project.created_at
    )

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return ProjectResponse(
        id=project.id,
        name=project.name,
        allowed_urls=json.loads(project.allowed_urls),
        test_count=0,
        created_at=project.created_at
    )

@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return None
