from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import typing as t
#from app.db.models import Setting
from . import models, schemas
from app.core.security import get_password_hash


# def get_user(db: Session, user_id: int):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(
#     db: Session, skip: int = 0, limit: int = 100
# ) -> t.List[schemas.UserOut]:
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     hashed_password = get_password_hash(user.password)
#     db_user = models.User(
#         first_name=user.first_name,
#         last_name=user.last_name,
#         email=user.email,
#         is_active=user.is_active,
#         is_superuser=user.is_superuser,
#         hashed_password=hashed_password,
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def delete_user(db: Session, user_id: int):
#     user = get_user(db, user_id)
#     if not user:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
#     db.delete(user)
#     db.commit()
#     return user


# def edit_user(
#     db: Session, user_id: int, user: schemas.UserEdit
# ) -> schemas.User:
#     db_user = get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
#     update_data = user.dict(exclude_unset=True)

#     if "password" in update_data:
#         update_data["hashed_password"] = get_password_hash(user.password)
#         del update_data["password"]

#     for key, value in update_data.items():
#         setattr(db_user, key, value)

#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# Job CRUD functions
def get_jobs(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.JobOut]:
    return db.query(models.Job).offset(skip).limit(limit).all()

def get_job(db: Session, job_id: int) -> schemas.JobOut:
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

def create_job(db: Session, job: schemas.JobCreate) -> schemas.JobOut:
    db_job = models.Job(
        date=job.date,
        client_job_no=job.client_job_no,
        client_asset_location=job.client_asset_location,
        previous_job_no=job.previous_job_no,
        date_received=job.date_received,
        make=job.make,
        type=job.type,
        site=job.site,
        job_no=job.job_no,
        client=job.client,
        client_ton_kks_ass_no=job.client_ton_kks_ass_no,
        date_delivered=job.date_delivered,
        frame_no=job.frame_no,
        ser_no=job.ser_no,
        hp=job.hp,
        kw=job.kw,
        rpm=job.rpm,
        phase=job.phase,
        volts=job.volts,
        amps=job.amps,
        hertz=job.hertz,
        ins_class=job.ins_class,
        duty=job.duty,
        winding_data=job.winding_data,
        slots_7=job.slots_7,
        poles=job.poles,
        pitch=job.pitch,
        original=job.original,
        modified=job.modified,
        core_length=job.core_length,
        core_ld_back_iron=job.core_ld_back_iron,
        total_coils=job.total_coils,
        total_sets=job.total_sets,
        coil_per_set=job.coil_per_set,
        wire_size=job.wire_size,
        no_of_wires_connection=job.no_of_wires_connection,
        jumper_wt_per_set=job.jumper_wt_per_set,
        total_wire_wt=job.total_wire_wt,
        winding_type=job.winding_type,
        lead_length=job.lead_length,
        lead_size=job.lead_size,
        no_of_leads=job.no_of_leads,
        lead_markings=job.lead_markings,
        bearing_de=job.bearing_de,
        bearing_nde=job.bearing_nde,
        shaft_dia=job.shaft_dia,
        slot_depth=job.slot_depth,
        tooth_width=job.tooth_width,
        rotor_dia=job.rotor_dia,
        calculated_gap=job.calculated_gap,
        rotor_slots=job.rotor_slots,
        slots_offset_angle=job.slots_offset_angle,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def delete_job(db: Session, job_id: int) -> schemas.JobOut:
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return job

def edit_job(db: Session, job_id: int, job: schemas.JobEdit) -> schemas.JobOut:
    db_job = get_job(db, job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    update_data = job.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job, key, value)

    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job
