from pydantic import BaseModel
import typing as t
from typing import Optional
from datetime import datetime, date


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

# Job Schemas
# Job Schemas
class Job(BaseModel):
    id: int  # Assuming there's an ID for the job
    date: str
    client_job_no: str
    client_asset_location: str
    previous_job_no: Optional[str] = None
    date_received: str
    make: str
    type: str
    site: str
    job_no: str
    client: str
    client_ton_kks_ass_no: str
    date_delivered: str
    frame_no: str
    ser_no: str
    hp: float
    kw: float
    rpm: int
    phase: int
    volts: float
    amps: float
    hertz: float
    ins_class: str
    duty: str
    winding_data: str
    slots_7: int
    poles: int
    pitch: float
    original: bool
    modified: bool
    core_length: float
    core_ld_back_iron: float
    total_coils: int
    total_sets: int
    coil_per_set: int
    wire_size: str
    no_of_wires_connection: int
    jumper_wt_per_set: float
    total_wire_wt: float
    winding_type: str
    lead_length: float
    lead_size: str
    no_of_leads: int
    lead_markings: str
    bearing_de: str
    bearing_nde: str
    shaft_dia: float
    slot_depth: float
    tooth_width: float
    rotor_dia: float
    calculated_gap: float
    rotor_slots: int
    slots_offset_angle: float

class JobBase(BaseModel):
    date: str
    client_job_no: str
    client_asset_location: str
    previous_job_no: t.Optional[str] = None
    date_received: str
    make: str
    type: str
    site: str
    job_no: str
    client: str
    client_ton_kks_ass_no: str
    date_delivered: str
    frame_no: str
    ser_no: str
    hp: float
    kw: float
    rpm: float
    phase: int
    volts: float
    amps: float
    hertz: float
    ins_class: str
    duty: str
    winding_data: str
    slots_7: int
    poles: int
    pitch: str
    original: str
    modified: str
    core_length: float
    core_ld_back_iron: float
    total_coils: int
    total_sets: int
    coil_per_set: int
    wire_size: str
    no_of_wires_connection: int
    jumper_wt_per_set: float
    total_wire_wt: float
    winding_type: str
    lead_length: float
    lead_size: str
    no_of_leads: int
    lead_markings: str
    bearing_de: str
    bearing_nde: str
    shaft_dia: float
    slot_depth: float
    tooth_width: float
    rotor_dia: float
    calculated_gap: float
    rotor_slots: int
    slots_offset_angle: float

class JobCreate(BaseModel):
    date: str
    client_job_no: str
    client_asset_location: str
    previous_job_no: str
    date_received: str
    make: str
    type: str
    site: str
    job_no: str
    client: str
    client_ton_kks_ass_no: str
    date_delivered: str
    frame_no: str
    ser_no: str
    hp: float
    kw: float
    rpm: int
    phase: int
    volts: float
    amps: float
    hertz: float
    ins_class: str
    duty: str
    winding_data: str
    slots_7: int
    poles: int
    pitch: float
    original: bool
    modified: bool
    core_length: float
    core_ld_back_iron: float
    total_coils: int
    total_sets: int
    coil_per_set: int
    wire_size: str
    no_of_wires_connection: int
    jumper_wt_per_set: float
    total_wire_wt: float
    winding_type: str
    lead_length: float
    lead_size: str
    no_of_leads: int
    lead_markings: str
    bearing_de: str
    bearing_nde: str
    shaft_dia: float
    slot_depth: float
    tooth_width: float
    rotor_dia: float
    calculated_gap: float
    rotor_slots: int
    slots_offset_angle: float

class JobOut(BaseModel):
    date: str
    client_job_no: str
    client_asset_location: str
    previous_job_no: str
    date_received: str
    make: str
    type: str
    site: str
    job_no: str
    client: str
    client_ton_kks_ass_no: str
    date_delivered: str
    frame_no: str
    ser_no: str
    hp: float
    kw: float
    rpm: int
    phase: int
    volts: float
    amps: float
    hertz: float
    ins_class: str
    duty: str
    winding_data: str
    slots_7: int
    poles: int
    pitch: float
    original: bool
    modified: bool
    core_length: float
    core_ld_back_iron: float
    total_coils: int
    total_sets: int
    coil_per_set: int
    wire_size: str
    no_of_wires_connection: int
    jumper_wt_per_set: float
    total_wire_wt: float
    winding_type: str
    lead_length: float
    lead_size: str
    no_of_leads: int
    lead_markings: str
    bearing_de: str
    bearing_nde: str
    shaft_dia: float
    slot_depth: float
    tooth_width: float
    rotor_dia: float
    calculated_gap: float
    rotor_slots: int
    slots_offset_angle: float

class JobEdit(BaseModel):
    date: Optional[str] = None
    client_job_no: Optional[str] = None
    client_asset_location: Optional[str] = None
    previous_job_no: Optional[str] = None
    date_received: Optional[str] = None
    make: Optional[str] = None
    type: Optional[str] = None
    site: Optional[str] = None
    job_no: Optional[str] = None
    client: Optional[str] = None
    client_ton_kks_ass_no: Optional[str] = None
    date_delivered: Optional[str] = None
    frame_no: Optional[str] = None
    ser_no: Optional[str] = None
    hp: Optional[float] = None
    kw: Optional[float] = None
    rpm: Optional[int] = None
    phase: Optional[int] = None
    volts: Optional[float] = None
    amps: Optional[float] = None
    hertz: Optional[float] = None
    ins_class: Optional[str] = None
    duty: Optional[str] = None
    winding_data: Optional[str] = None
    slots_7: Optional[int] = None
    poles: Optional[int] = None
    pitch: Optional[float] = None
    original: Optional[bool] = None
    modified: Optional[bool] = None
    core_length: Optional[float] = None
    core_ld_back_iron: Optional[float] = None
    total_coils: Optional[int] = None
    total_sets: Optional[int] = None
    coil_per_set: Optional[int] = None
    wire_size: Optional[str] = None
    no_of_wires_connection: Optional[int] = None
    jumper_wt_per_set: Optional[float] = None
    total_wire_wt: Optional[float] = None
    winding_type: Optional[str] = None
    lead_length: Optional[float] = None
    lead_size: Optional[str] = None
    no_of_leads: Optional[int] = None
    lead_markings: Optional[str] = None
    bearing_de: Optional[str] = None
    bearing_nde: Optional[str] = None
    shaft_dia: Optional[float] = None
    slot_depth: Optional[float] = None
    tooth_width: Optional[float] = None
    rotor_dia: Optional[float] = None
    calculated_gap: Optional[float] = None
    rotor_slots: Optional[int] = None
    slots_offset_angle: Optional[float] = None

    class Config:
        orm_mode = True