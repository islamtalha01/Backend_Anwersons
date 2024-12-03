from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class SeverityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class IssueBase(BaseModel):
    description: Optional[str] = None
    project_issue_id: int
    image_id: Optional[str] = None
    image_url: Optional[str] = None


class IssueCreate(IssueBase):
    pass

class IssueUpdate(IssueBase):
    title: Optional[str] = None  # All fields optional for partial updates


class IssueResponse(IssueBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class IssueDetailResponse(BaseModel):
    issue: Optional[IssueResponse]
