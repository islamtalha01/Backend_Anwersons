from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from database.db import get_db  # Database session dependency
from database.models import Issue, Project, ProjectIssue  # Import the Issue and Project models
from schemas.issue_schemas import (
    IssueCreate,
    IssueUpdate,
    IssueResponse,
    IssueDetailResponse
)  # Import schemas for the Issue model

router = APIRouter()



# Create a new issue
@router.post("/", response_model=IssueResponse)
async def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    try:
        # Validate project existence
        project = db.query(ProjectIssue).filter(ProjectIssue.id == issue.project_issue_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Create a new Issue instance
        new_issue = Issue(
            title=issue.title,
            description=issue.description,
            steps_to_reproduce=issue.steps_to_reproduce,
            expected_behaviour=issue.expected_behaviour,
            actual_behaviour=issue.actual_behaviour,
            severity=issue.severity,
            issue_metadata=issue.issue_metadata,
            project_issue_id=issue.project_issue_id,
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
        raise HTTPException(status_code=500, detail=f"Error creating issue: {str(e)}")


# Get all issues for a project
@router.get("/project-issue/{project_issue_id}", response_model=List[IssueResponse])
async def get_issues_for_project(project_issue_id: int, db: Session = Depends(get_db)):
    # Validate project existence
    project = db.query(ProjectIssue).filter(ProjectIssue.id == project_issue_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Fetch issues associated with the project
    issues = db.query(Issue).filter(Issue.project_issue_id == project_issue_id).all()
    if not issues:
        # raise HTTPException(status_code=404, detail="No issues found for the specified project")
        return []

    return issues


# Get issue details by ID
@router.get("/{issue_id}", response_model=IssueDetailResponse)
async def get_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        # raise HTTPException(status_code=404, detail="Issue not found")
        return {}
    return issue


# Update an issue
@router.put("/{issue_id}", response_model=IssueResponse)
async def update_issue(issue_id: int, issue_update: IssueUpdate, db: Session = Depends(get_db)):
    # Find the issue by ID
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not db_issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Update issue fields
    for field, value in issue_update.model_dump(exclude_unset=True).items():
        setattr(db_issue, field, value)
        print("Field: ", field)
        print("Value: ", value)
    db_issue.updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(db_issue)
        return db_issue
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail=f"Error updating issue: {str(e)}")


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
        raise HTTPException(status_code=500, detail=f"Error deleting issue: {str(e)}")
