from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import enum

class TicketCreate(BaseModel):
    title : str
    description : str
    # position : int
    list_id : int
    project_id : int
    assignee : str
    priority : str = "medium"
    status : str = "new"
    due_date : Optional[datetime]
    labels : List[str] = []
    edit_mode : bool = False
    
class TicketResponse(BaseModel):
    id: int
    title : str
    description : str
    position : int
    list_id : int
    project_id : int
    assignee : str
    priority : str
    status : str
    due_date : Optional[datetime]
    labels : List[str]
    edit_mode : bool
    created_at : str
    updated_at : str
    
# class TicketMove(BaseModel):
#     source_list_id: str
#     destination_list_id: str
#     # position: int
#     source_position_in_list: int
#     destination_position_in_list: int
    
class TicketReorderItem(BaseModel):
    id: int
    source_list_id: int
    destination_list_id: int
    position: int

class TicketReorderRequest(BaseModel):
    tickets: List[TicketReorderItem]