from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from database.db import get_db  # Database session dependency
from database.models import Job  # SQLAlchemy model for "projects"
from schemas.jobs import JobCreate, JobEdit, JobResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/jobs", response_model=List[JobResponse])
def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of jobs with optional skip and limit.
    """
    return db.query(Job).offset(skip).limit(limit).all()

@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific job by ID.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/jobs", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """
    Create a new job with the provided details.
    """
    db_job = Job(
        date=job.date,
        name = job.name,
        description = job.description
        # date=job.date,
        # client_job_no=job.client_job_no,
        # client_asset_location=job.client_asset_location,
        # previous_job_no=job.previous_job_no,
        # date_received=job.date_received,
        # make=job.make,
        # type=job.type,
        # site=job.site,
        # job_no=job.job_no,
        # client=job.client,
        # client_ton_kks_ass_no=job.client_ton_kks_ass_no,
        # date_delivered=job.date_delivered,
        # frame_no=job.frame_no,
        # ser_no=job.ser_no,
        # hp=job.hp,
        # kw=job.kw,
        # rpm=job.rpm,
        # phase=job.phase,
        # volts=job.volts,
        # amps=job.amps,
        # hertz=job.hertz,
        # ins_class=job.ins_class,
        # duty=job.duty,
        # winding_data=job.winding_data,
        # slots=job.slots,
        # poles=job.poles,
        # pitch=job.pitch,
        # core_length=job.core_length,
        # core_ld_back_iron=job.core_ld_back_iron,
        # total_coils=job.total_coils,
        # total_sets=job.total_sets,
        # coil_per_set=job.coil_per_set,
        # wire_size=job.wire_size,
        # no_of_wires_connection=job.no_of_wires_connection,
        # jumper_wt_per_set=job.jumper_wt_per_set,
        # total_wire_wt=job.total_wire_wt,
        # winding_type=job.winding_type,
        # lead_length=job.lead_length,
        # lead_size=job.lead_size,
        # no_of_leads=job.no_of_leads,
        # lead_markings=job.lead_markings,
        # bearing_de=job.bearing_de,
        # bearing_nde=job.bearing_nde,
        # shaft_dia=job.shaft_dia,
        # slot_depth=job.slot_depth,
        # tooth_width=job.tooth_width,
        # rotor_dia=job.rotor_dia,
        # calculated_gap=job.calculated_gap,
        # rotor_slots=job.rotor_slots,
        # slots_offset_angle=job.slots_offset_angle,
    )

    try:
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        logger.info(f"Job created successfully: {db_job}")
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error creating job: {e.orig}")
        raise HTTPException(status_code=400, detail="Job creation failed")
    
    return db_job

@router.delete("/jobs/{job_id}", response_model=JobResponse)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """
    Delete a job by ID.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return job

@router.put("/jobs/{job_id}", response_model=JobResponse)
def edit_job(job_id: int, job: JobEdit, db: Session = Depends(get_db)):
    """
    Update an existing job by ID with the provided details.
    """
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    for key, value in job.dict(exclude_unset=True).items():
        setattr(db_job, key, value)
    
    try:
        db.commit()
        db.refresh(db_job)
        logger.info(f"Job updated successfully: {db_job}")
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error updating job: {e.orig}")
        raise HTTPException(status_code=400, detail="Job update failed")
    
    return db_job








# from datetime import datetime, timezone
# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session
# from typing import List
# from database.db import get_db  # Database session dependency
# from database.models import Job as Job  # SQLAlchemy model for "projects"

# from schemas.jobs import JobCreate, JobEdit, JobResponse

# router = APIRouter()






# def get_jobs(
#     db: Session, skip: int = 0, limit: int = 100
# ) -> List[JobResponse]:
#     return db.query(Job).offset(skip).limit(limit).all()

# def get_job(db: Session, job_id: int) -> JobResponse:
#     job = db.query(Job).filter(Job.id == job_id).first()
#     if not job:
#         raise HTTPException(status_code=404, detail="Job not found")
#     return job

# def create_job(db: Session, job: JobCreate) -> JobResponse:
#     db_job =Job(
#         date=job.date,
#         client_job_no=job.client_job_no,
#         client_asset_location=job.client_asset_location,
#         previous_job_no=job.previous_job_no,
#         date_received=job.date_received,
#         make=job.make,
#         type=job.type,
#         site=job.site,
#         job_no=job.job_no,
#         client=job.client,
#         client_ton_kks_ass_no=job.client_ton_kks_ass_no,
#         date_delivered=job.date_delivered,
#         frame_no=job.frame_no,
#         ser_no=job.ser_no,
#         hp=job.hp,
#         kw=job.kw,
#         rpm=job.rpm,
#         phase=job.phase,
#         volts=job.volts,
#         amps=job.amps,
#         hertz=job.hertz,
#         ins_class=job.ins_class,
#         duty=job.duty,
#         winding_data=job.winding_data,
#         slots=job.slots,
#         poles=job.poles,
#         pitch=job.pitch,
#         core_length=job.core_length,
#         core_ld_back_iron=job.core_ld_back_iron,
#         total_coils=job.total_coils,
#         total_sets=job.total_sets,
#         coil_per_set=job.coil_per_set,
#         wire_size=job.wire_size,
#         no_of_wires_connection=job.no_of_wires_connection,
#         jumper_wt_per_set=job.jumper_wt_per_set,
#         total_wire_wt=job.total_wire_wt,
#         winding_type=job.winding_type,
#         lead_length=job.lead_length,
#         lead_size=job.lead_size,
#         no_of_leads=job.no_of_leads,
#         lead_markings=job.lead_markings,
#         bearing_de=job.bearing_de,
#         bearing_nde=job.bearing_nde,
#         shaft_dia=job.shaft_dia,
#         slot_depth=job.slot_depth,
#         tooth_width=job.tooth_width,
#         rotor_dia=job.rotor_dia,
#         calculated_gap=job.calculated_gap,
#         rotor_slots=job.rotor_slots,
#         slots_offset_angle=job.slots_offset_angle,
#     )
    
#     try:
#         db.add(db_job)
#         db.commit()
#         db.refresh(db_job)
#         logger.info(f"Job created successfully: {db_job}")
#     except IntegrityError as e:
#         db.rollback()
#         logger.error(f"Error creating job: {e.orig}")
#         raise
    
#     return schemas.JobOut.from_orm(db_job)  # Assuming you have a method for conversion

# def delete_job(db: Session, job_id: int) -> JobResponse:
#     job = get_job(db, job_id)
#     if not job:
#         raise HTTPException(status_code=404, detail="Job not found")
#     db.delete(job)
#     db.commit()
#     return job

# def edit_job(db: Session, job_id: int, job: JobEdit) -> JobResponse:
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












# @router.post("/", response_model=ProjectResponse)
# async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
#     try:
#         # Create a new Project instance
#         new_project = Project(
#             name=project.name,
#             description=project.description,
#             members=project.members,
#             created_at=datetime.now(timezone.utc),
#             updated_at=datetime.now(timezone.utc),
#             user_id = project.user_id
#         )

#         # Add the new project to the database
#         db.add(new_project)
#         db.commit()
#         db.refresh(new_project)  # Refresh to get the new project's ID and other fields

#         return new_project
#     except Exception as e:
#         print(e)  # Optional: Log the exception for debugging
#         raise HTTPException(status_code=500, detail="Error creating project")


# @router.get("/", response_model=List[ProjectResponse])
# async def get_all_projects(db: Session = Depends(get_db)):
#     # Fetch all projects from the database
#     projects = db.query(Project).all()
#     if not projects:
#         return []
#         # raise HTTPException(status_code=404, detail="No projects found")
#     return projects


# @router.get("/user/{user_id}", response_model=List[ProjectResponse])
# async def get_user_projects(db: Session = Depends(get_db), user_id: str = None):
#     # Fetch all projects from the database
#     projects = db.query(Project).filter(Project.user_id == user_id).all()
#     if not projects:
#         return []
#         # raise HTTPException(status_code=404, detail="No projects found")
#     return projects


# @router.get("/{project_id}", response_model=ProjectDetailResponse)
# async def get_project_with_lists_and_tickets(project_id: int, db: Session = Depends(get_db)):
#     # Fetch the project
#     project = db.query(Project).filter(Project.id == project_id).first()
#     if not project:
#         # raise HTTPException(status_code=404, detail="Project not found")
#         return []

#     # Fetch the lists associated with the project
#     project_lists = db.query(ListModel).filter(ListModel.project_id == project_id).all()
#     print(project_lists)
#     # Fetch tickets for each list and map them to their respective lists
#     lists_with_tickets = []
#     for list_item in project_lists:
#         tickets = db.query(Ticket).filter(Ticket.list_id == list_item.id).all()
#         lists_with_tickets.append({
#             "id": list_item.id,
#             "name": list_item.name,
#             "project_id": list_item.project_id,
#             "position": list_item.position,
#             "created_at": list_item.created_at,
#             "updated_at": list_item.updated_at,
#             "tickets": tickets
#         })

#     # Construct the response
#     return {
#         "id": project.id,
#         "name": project.name,
#         "description": project.description,
#         "lists": lists_with_tickets
#     }



# @router.put("/{project_id}", response_model=ProjectResponse)
# async def update_project(project_id: int, project: ProjectCreate, db: Session = Depends(get_db)):
#     # Find the project by ID
#     db_project = db.query(Project).filter(Project.id == project_id).first()

#     if not db_project:
#         # raise HTTPException(status_code=404, detail="Project not found")
#         return []

#     # Update the project fields
#     db_project.name = project.name
#     db_project.description = project.description
#     db_project.members = project.members
#     db_project.updated_at = datetime.now(timezone.utc)

#     try:
#         # Commit the changes to the database
#         db.commit()
#         db.refresh(db_project)  # Refresh to get the updated fields

#         return db_project
#     except Exception as e:
#         db.rollback()  # Roll back the transaction in case of an error
#         print(e)  # Log the exception for debugging
#         raise HTTPException(status_code=500, detail="Error updating project")


# @router.delete("/{project_id}")
# async def delete_project(project_id: int, db: Session = Depends(get_db)):
    
#     # Delete related tickets first
#     db.query(Ticket).filter(Ticket.project_id == project_id).delete()
#     # Delete related lists first
#     db.query(ListModel).filter(ListModel.project_id == project_id).delete()
#     db.commit()  # Commit deletion of related lists

#     # Delete the project
#     project_deleted = db.query(Project).filter(Project.id == project_id).delete()
#     db.commit()  # Commit deletion of the project

#     if project_deleted:
#         return {"message": "Project deleted successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="Project not found")
