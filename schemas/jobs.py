


from pydantic import BaseModel
import typing as t
from typing import Optional
from datetime import datetime, date




class Config:
        arbitrary_types_allowed = True

# Job Schemas
# class Job(BaseModel):
#     id: Optional[int]  # Assuming there's an ID for the job
#     date: Optional[str] = None
#     client_job_no: Optional[str] = None
#     client_asset_location: Optional[str] = None
#     previous_job_no: Optional[str] = None
#     date_received: Optional[str] = None
#     make: Optional[str] = None
#     type: Optional[str] = None
#     site: Optional[str] = None
#     job_no: Optional[str] = None
#     client: Optional[str] = None
#     client_ton_kks_ass_no: Optional[str] = None
#     date_delivered: Optional[str] = None
#     frame_no: Optional[str] = None
#     ser_no: Optional[str] = None
#     hp: Optional[float] = None
#     kw: Optional[float] = None
#     rpm: Optional[int] = None
#     phase: Optional[int] = None
#     volts: Optional[float] = None
#     amps: Optional[float] = None
#     hertz: Optional[float] = None
#     ins_class: Optional[str] = None
#     duty: Optional[str] = None
#     winding_data: Optional[str] = None
#     slots: Optional[int] = None
#     poles: Optional[int] = None
#     pitch: Optional[float] = None
#     core_length: Optional[float] = None
#     core_ld_back_iron: Optional[float] = None
#     total_coils: Optional[int] = None
#     total_sets: Optional[int] = None
#     coil_per_set: Optional[int] = None
#     wire_size: Optional[float] = None
#     no_of_wires_connection: Optional[int] = None
#     jumper_wt_per_set: Optional[float] = None
#     total_wire_wt: Optional[float] = None
#     winding_type: Optional[str] = None
#     lead_length: Optional[float] = None
#     lead_size: Optional[float] = None
#     no_of_leads: Optional[int] = None
#     lead_markings: Optional[str] = None
#     bearing_de: Optional[str] = None
#     bearing_nde: Optional[str] = None
#     shaft_dia: Optional[float] = None
#     slot_depth: Optional[float] = None
#     tooth_width: Optional[float] = None
#     rotor_dia: Optional[float] = None
#     calculated_gap: Optional[float] = None
#     rotor_slots: Optional[int] = None
#     slots_offset_angle: Optional[float] = None

class Job(BaseModel):
     
    date:Optional[str] = None # Changed from Date to String
    name : Optional[str] = None
    description:Optional[str] = None

    # date: Optional[str] = None
    # client_job_no: Optional[str] = None
    # client_asset_location: Optional[str] = None
    # previous_job_no: Optional[str] = None
    # date_received: Optional[str] = None
    # make: Optional[str] = None
    # type: Optional[str] = None
    # site: Optional[str] = None
    # job_no: Optional[str] = None
    # client: Optional[str] = None
    # client_ton_kks_ass_no: Optional[str] = None
    # date_delivered: Optional[str] = None
    # frame_no: Optional[str] = None
    # ser_no: Optional[str] = None
    # hp: Optional[float] = None
    # kw: Optional[float] = None
    # rpm: Optional[int] = None
    # phase: Optional[int] = None
    # volts: Optional[float] = None
    # amps: Optional[float] = None
    # hertz: Optional[float] = None
    # ins_class: Optional[str] = None
    # duty: Optional[str] = None
    # winding_data: Optional[str] = None
    # slots: Optional[int] = None
    # poles: Optional[int] = None
    # pitch: Optional[float] = None
    # core_length: Optional[float] = None
    # core_ld_back_iron: Optional[float] = None
    # total_coils: Optional[int] = None
    # total_sets: Optional[int] = None
    # coil_per_set: Optional[int] = None
    # wire_size: Optional[float] = None
    # no_of_wires_connection: Optional[int] = None
    # jumper_wt_per_set: Optional[float] = None
    # total_wire_wt: Optional[float] = None
    # winding_type: Optional[str] = None
    # lead_length: Optional[float] = None
    # lead_size: Optional[float] = None
    # no_of_leads: Optional[int] = None
    # lead_markings: Optional[str] = None
    # bearing_de: Optional[str] = None
    # bearing_nde: Optional[str] = None
    # shaft_dia: Optional[float] = None
    # slot_depth: Optional[float] = None
    # tooth_width: Optional[float] = None
    # rotor_dia: Optional[float] = None
    # calculated_gap: Optional[float] = None
    # rotor_slots: Optional[int] = None
    # slots_offset_angle: Optional[float] = None

class JobCreate(Job):
    pass  # All fields inherited from JobBase

class JobEdit(Job):
    pass  # All fields inherited from JobBase

class JobResponse(Job):
    id: int  # Assuming id is required for the output

    class Config:
        orm_mode = True  # Allow Pydantic to parse ORM models
        from_attributes = True  # Enable from_orm support