from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from database.db import get_db  # Dependency for DB session
from database.models import ProjectIssue  # SQLAlchemy model
from schemas.project_issue_schemas import (
    ProjectIssueCreate,
    ProjectIssueUpdate,
    ProjectIssueResponse,
    ProjectIssueDetailResponse,
)

router = APIRouter()


# Create a new ProjectIssue
@router.post("/", response_model=ProjectIssueResponse)
async def create_project_issue(project_issue: ProjectIssueCreate, db: Session = Depends(get_db)):
    try:
        new_project_issue = ProjectIssue(
            name=project_issue.name,
            website=project_issue.website,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(new_project_issue)
        db.commit()
        db.refresh(new_project_issue)
        return new_project_issue
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating project issue")


# Get all ProjectIssues
@router.get("/", response_model=List[ProjectIssueResponse])
async def get_all_project_issues(db: Session = Depends(get_db)):
    project_issues = db.query(ProjectIssue).all()
    if not project_issues:
        raise HTTPException(status_code=404, detail="No project issues found")
    return project_issues


# Get a single ProjectIssue by ID
@router.get("/{project_issue_id}", response_model=ProjectIssueDetailResponse)
async def get_ProjectIssue_issues(project_issue_id: int, db: Session = Depends(get_db)):
    project_issue = db.query(ProjectIssue).filter(ProjectIssue.id == project_issue_id).first()
    if not project_issue:
        raise HTTPException(status_code=404, detail="Project issue not found")
    return project_issue


# Update a ProjectIssue
@router.put("/{project_issue_id}", response_model=ProjectIssueResponse)
async def update_project_issue(
    project_issue_id: int, project_issue_update: ProjectIssueUpdate, db: Session = Depends(get_db)
):
    project_issue = db.query(ProjectIssue).filter(ProjectIssue.id == project_issue_id).first()
    if not project_issue:
        raise HTTPException(status_code=404, detail="Project issue not found")

    for field, value in project_issue_update.dict(exclude_unset=True).items():
        setattr(project_issue, field, value)
    project_issue.updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(project_issue)
        return project_issue
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Error updating project issue")


# Delete a ProjectIssue
@router.delete("/{project_issue_id}")
async def delete_project_issue(project_issue_id: int, db: Session = Depends(get_db)):
    project_issue = db.query(ProjectIssue).filter(ProjectIssue.id == project_issue_id).first()
    if not project_issue:
        raise HTTPException(status_code=404, detail="Project issue not found")

    try:
        db.delete(project_issue)
        db.commit()
        return {"message": "Project issue deleted successfully"}
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Error deleting project issue")
