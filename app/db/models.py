from sqlalchemy import Boolean, Column, Integer, String, Float, Date, DateTime, func
from .session import Base

# User model
# class User(Base):
#     __tablename__ = "user"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     first_name = Column(String)
#     last_name = Column(String)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, default=True)
#     is_superuser = Column(Boolean, default=False)

# # Setting model
# class Setting(Base):
#     __tablename__ = "settings"

#     id = Column(Integer, primary_key=True, index=True)
#     key = Column(String, unique=True, index=True, nullable=False)  # Setting key (e.g., "site_name")
#     value = Column(String, nullable=False)                          # Setting value (e.g., "My Website")
#     description = Column(String)                                   # Optional description of the setting
#     data_type = Column(String)                                     # Type of the setting (e.g., "string", "boolean", "integer", "float")
#     is_active = Column(Boolean, default=True)                     # Flag to indicate if the setting is active
#     created_at = Column(DateTime, server_default=func.now())     # Timestamp when the setting was created
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())  # Timestamp for the last update


# Job model
class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)  # Changed from Date to String
    client_job_no = Column(String)
    client_asset_location = Column(String)
    previous_job_no = Column(String, nullable=True)
    date_received = Column(String)  # Changed from Date to String
    make = Column(String)
    type = Column(String)
    site = Column(String)
    job_no = Column(String)
    client = Column(String)
    client_ton_kks_ass_no = Column(String)
    date_delivered = Column(String)  # Changed from Date to String
    frame_no = Column(String)
    ser_no = Column(String)
    hp = Column(Float)
    kw = Column(Float)
    rpm = Column(Float)
    phase = Column(Integer)
    volts = Column(Float)
    amps = Column(Float)
    hertz = Column(Float)
    ins_class = Column(String)
    duty = Column(String)
    winding_data = Column(String)
    slots_7 = Column(Integer)
    poles = Column(Integer)
    pitch = Column(String)
    core_length = Column(Float)
    core_ld_back_iron = Column(Float)
    total_coils = Column(Integer)
    total_sets = Column(Integer)
    coil_per_set = Column(Integer)
    wire_size = Column(Float)
    no_of_wires_connection = Column(Integer)
    jumper_wt_per_set = Column(Float)
    total_wire_wt = Column(Float)
    winding_type = Column(String)
    lead_length = Column(Float)
    lead_size = Column(Float)
    no_of_leads = Column(Integer)
    lead_markings = Column(String)
    bearing_de = Column(String)
    bearing_nde = Column(String)
    shaft_dia = Column(Float)
    slot_depth = Column(Float)
    tooth_width = Column(Float)
    rotor_dia = Column(Float)
    calculated_gap = Column(Float)
    rotor_slots = Column(Integer)
    slots_offset_angle = Column(Float)