from typing import List, Optional
from pydantic import BaseModel
from schemas.ticket_schemas import TicketResponse
from datetime import datetime


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    members: List[str] = ["admin"]  # Default to admin user
    user_id: str



class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    members: List[str]
    created_at: datetime
    updated_at: datetime
    user_id: str
    

class ListWithTickets(BaseModel):
    id: int
    name: str
    project_id: int
    created_at: datetime
    updated_at: datetime
    tickets: List[TicketResponse]  # List of tickets for the list

    class Config:
        orm_mode = True


class ProjectDetailResponse(BaseModel):
    id: int
    name: str
    description: str
    lists: List[ListWithTickets]  # Lists associated with the project

    class Config:
        orm_mode = True