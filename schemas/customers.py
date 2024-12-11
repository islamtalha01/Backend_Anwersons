from pydantic import BaseModel
from datetime import datetime
import typing as t
from typing import Optional



class Config:
        arbitrary_types_allowed = True

# Shared base schema
class CustomerBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


# Schema for creating a new customer
class CustomerCreate(CustomerBase):
    pass  # Reuse the base fields as is


# Schema for editing an existing customer (all fields optional)
class CustomerEdit(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


# Schema for responding with customer data
class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # This tells Pydantic to work with SQLAlchemy models
