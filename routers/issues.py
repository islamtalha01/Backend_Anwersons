from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from database.db import get_db  # Database session dependency
from database.models import Issue, Project  # Import the Issue and Project models
from schemas.issue_schemas import (
    IssueCreate,
    IssueUpdate,
    IssueResponse,
    IssueDetailResponse
)  # Import schemas for the Issue model
import json

router = APIRouter()

# Create a new issue
@router.post("/", response_model=IssueResponse)
async def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    try:
        # Validate project existence
        project = db.query(Project).filter(Project.id == issue.project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        print("Metadata: ",issue.issue_metadata )
        print("Type of issue_metadata:", type(issue.issue_metadata))

        # Create a new Issue instance
        new_issue = Issue(
            title=issue.title,
            description=issue.description,
            steps_to_reproduce=issue.steps_to_reproduce,
            expected_behaviour=issue.expected_behaviour,
            actual_behaviour=issue.actual_behaviour,
            severity=issue.severity,
            metadata=json.dumps(issue.issue_metadata),
            project_id=issue.project_id,
            image_id=issue.image_id,
            image_url=issue.image_url,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        # Add the new issue to the database
        db.add(new_issue)
        db.commit()
        db.refresh(new_issue)

        return new_issue
    except Exception as e:
        print(e)  # Optional: Log the exception for debugging
        raise HTTPException(status_code=500, detail="Error creating issue")


# Get all issues for a project
@router.get("/project/{project_id}", response_model=List[IssueResponse])
async def get_issues_for_project(project_id: int, db: Session = Depends(get_db)):
    # Validate project existence
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Fetch issues associated with the project
    issues = db.query(Issue).filter(Issue.project_id == project_id).all()
    if not issues:
        raise HTTPException(status_code=404, detail="No issues found for the specified project")

    return issues


# Get issue details by ID
@router.get("/{issue_id}", response_model=IssueDetailResponse)
async def get_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


# Update an issue
@router.put("/{issue_id}", response_model=IssueResponse)
async def update_issue(issue_id: int, issue_update: IssueUpdate, db: Session = Depends(get_db)):
    # Find the issue by ID
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not db_issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Update issue fields
    for field, value in issue_update.dict(exclude_unset=True).items():
        setattr(db_issue, field, value)
    db_issue.updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(db_issue)
        return db_issue
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Error updating issue")


# Delete an issue
@router.delete("/{issue_id}")
async def delete_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    try:
        db.delete(issue)
        db.commit()
        return {"message": "Issue deleted successfully"}
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Error deleting issue")
