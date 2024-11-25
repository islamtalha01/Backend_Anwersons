from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .issue_schemas import IssueResponse

class ProjectIssueBase(BaseModel):
    name: str
    website: Optional[str] = None


class ProjectIssueCreate(ProjectIssueBase):
    pass


class ProjectIssueUpdate(ProjectIssueBase):
    name: Optional[str] = None
    website: Optional[str] = None


class ProjectIssueResponse(ProjectIssueBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        
class ProjectIssueDetailResponse(ProjectIssueResponse):
    issues: List[IssueResponse]
    pass
