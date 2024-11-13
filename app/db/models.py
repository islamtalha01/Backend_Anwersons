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
    date = Column(String, nullable=True)  # Changed from Date to String
    client_job_no = Column(String, nullable=True)
    client_asset_location = Column(String, nullable=True)
    previous_job_no = Column(String, nullable=True)
    date_received = Column(String, nullable=True)  # Changed from Date to String
    make = Column(String, nullable=True)
    type = Column(String, nullable=True)
    site = Column(String, nullable=True)
    job_no = Column(String, nullable=True)
    client = Column(String, nullable=True)
    client_ton_kks_ass_no = Column(String, nullable=True)
    date_delivered = Column(String, nullable=True)  # Changed from Date to String
    frame_no = Column(String, nullable=True)
    ser_no = Column(String, nullable=True)
    hp = Column(Float, nullable=True)
    kw = Column(Float, nullable=True)
    rpm = Column(Float, nullable=True)
    phase = Column(Integer, nullable=True)
    volts = Column(Float, nullable=True)
    amps = Column(Float, nullable=True)
    hertz = Column(Float, nullable=True)
    ins_class = Column(String, nullable=True)
    duty = Column(String, nullable=True)
    winding_data = Column(String, nullable=True)
    slots = Column(Integer, nullable=True)
    poles = Column(Integer, nullable=True)
    pitch = Column(String, nullable=True)
    core_length = Column(Float, nullable=True)
    core_ld_back_iron = Column(Float, nullable=True)
    total_coils = Column(Integer, nullable=True)
    total_sets = Column(Integer, nullable=True)
    coil_per_set = Column(Integer, nullable=True)
    wire_size = Column(Float, nullable=True)
    no_of_wires_connection = Column(Integer, nullable=True)
    jumper_wt_per_set = Column(Float, nullable=True)
    total_wire_wt = Column(Float, nullable=True)
    winding_type = Column(String, nullable=True)
    lead_length = Column(Float, nullable=True)
    lead_size = Column(Float, nullable=True)
    no_of_leads = Column(Integer, nullable=True)
    lead_markings = Column(String, nullable=True)
    bearing_de = Column(String, nullable=True)
    bearing_nde = Column(String, nullable=True)
    shaft_dia = Column(Float, nullable=True)
    slot_depth = Column(Float, nullable=True)
    tooth_width = Column(Float, nullable=True)
    rotor_dia = Column(Float, nullable=True)
    calculated_gap = Column(Float, nullable=True)
    rotor_slots = Column(Integer, nullable=True)
    slots_offset_angle = Column(Float, nullable=True)