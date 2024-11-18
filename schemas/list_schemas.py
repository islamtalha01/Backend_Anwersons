from typing import List, Optional
from pydantic import BaseModel


class ListCreate(BaseModel):
    project_id: int
    name: str
    # position: Optional[int] = None
    
    
    
class ListResponse(BaseModel):
    id: int
    project_id: int
    name: str
    position: Optional[int] = None
    created_at: str
    updated_at: str
    
class ListsResponse(BaseModel):
    lists: List[ListResponse]
    
    
class ListReorderItem(BaseModel):
    id: int
    position: int

class ListReorderRequest(BaseModel):
    lists: List[ListReorderItem]
