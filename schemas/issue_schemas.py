from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class SeverityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class IssueBase(BaseModel):
    title: str
    description: Optional[str] = None
    steps_to_reproduce: Optional[list] = None
    expected_behaviour: Optional[str] = None
    actual_behaviour: Optional[str] = None
    severity: SeverityEnum
    issue_metadata: Optional[dict] = None
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


class IssueDetailResponse(IssueResponse):
    pass
