from sqlalchemy import (
    Column, Integer, String, Float, TIMESTAMP, Boolean, Enum, JSON
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()








class Job(Base):
    __tablename__ = "job"


    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=True)  # Changed from Date to String
    name  = Column(String, nullable=True)
    description  = Column(String, nullable=True)


    # id = Column(Integer, primary_key=True, index=True)
    # date = Column(TIMESTAMP, default=datetime.now(timezone.utc))  # Changed from Date to String
    # client_job_no = Column(String, nullable=True)
    # client_asset_location = Column(String, nullable=True)
    # previous_job_no = Column(String, nullable=True)
    # date_received = Column(String, nullable=True)  # Changed from Date to String
    # make = Column(String, nullable=True)
    # type = Column(String, nullable=True)
    # site = Column(String, nullable=True)
    # job_no = Column(String, nullable=True)
    # client = Column(String, nullable=True)
    # client_ton_kks_ass_no = Column(String, nullable=True)
    # date_delivered = Column(String, nullable=True)  # Changed from Date to String
    # frame_no = Column(String, nullable=True)
    # ser_no = Column(String, nullable=True)
    # hp = Column(Float, nullable=True)
    # kw = Column(Float, nullable=True)
    # rpm = Column(Float, nullable=True)
    # phase = Column(Integer, nullable=True)
    # volts = Column(Float, nullable=True)
    # amps = Column(Float, nullable=True)
    # hertz = Column(Float, nullable=True)
    # ins_class = Column(String, nullable=True)
    # duty = Column(String, nullable=True)
    # winding_data = Column(String, nullable=True)
    # slots = Column(Integer, nullable=True)
    # poles = Column(Integer, nullable=True)
    # pitch = Column(String, nullable=True)
    # core_length = Column(Float, nullable=True)
    # core_ld_back_iron = Column(Float, nullable=True)
    # total_coils = Column(Integer, nullable=True)
    # total_sets = Column(Integer, nullable=True)
    # coil_per_set = Column(Integer, nullable=True)
    # wire_size = Column(Float, nullable=True)
    # no_of_wires_connection = Column(Integer, nullable=True)
    # jumper_wt_per_set = Column(Float, nullable=True)
    # total_wire_wt = Column(Float, nullable=True)
    # winding_type = Column(String, nullable=True)
    # lead_length = Column(Float, nullable=True)
    # lead_size = Column(Float, nullable=True)
    # no_of_leads = Column(Integer, nullable=True)
    # lead_markings = Column(String, nullable=True)
    # bearing_de = Column(String, nullable=True)
    # bearing_nde = Column(String, nullable=True)
    # shaft_dia = Column(Float, nullable=True)
    # slot_depth = Column(Float, nullable=True)
    # tooth_width = Column(Float, nullable=True)
    # rotor_dia = Column(Float, nullable=True)
    # calculated_gap = Column(Float, nullable=True)
    # rotor_slots = Column(Integer, nullable=True)
    # slots_offset_angle = Column(Float, nullable=True)
    # created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    # updated_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))











