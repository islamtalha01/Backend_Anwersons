# from pydantic import BaseModel
# import typing as t
# from datetime import datetime


# class UserBase(BaseModel):
#     email: str
#     is_active: bool = True
#     is_superuser: bool = False
#     first_name: str = None
#     last_name: str = None


# class UserOut(UserBase):
#     pass


# class UserCreate(UserBase):
#     password: str

#     class Config:
#         orm_mode = True


# class UserEdit(UserBase):
#     password: t.Optional[str] = None

#     class Config:
#         orm_mode = True


# class User(UserBase):
#     id: int

#     class Config:
#         orm_mode = True


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     email: str = None
#     permissions: str = "user"



# #settings schemas


# class SettingBase(BaseModel):
#     key: str
#     value: str

# class SettingCreate(SettingBase):
#     pass

# class SettingUpdate(BaseModel):
#     value: str

# class SettingInDB(SettingBase):
#     id: int

#     class Config:
#         orm_mode = True


# #Agent Schema
# class AgentBase(BaseModel):
#     name: str
#     model_name: str
#     key: str
#     temperature: float
#     prompt: str
#     status: bool

# class AgentCreate(AgentBase):
#     pass

# class AgentUpdate(AgentBase):
#     pass

# class Agent(AgentBase):
#     id: int
#     date_created: datetime

#     class Config:
#         orm_mode = True



from pydantic import BaseModel
from typing import Optional
from datetime import date

class FlightDataBase(BaseModel):
    from_city: str
    to_city: str
    departure_date: date
    return_date: Optional[date] = None
    fare_amount: float