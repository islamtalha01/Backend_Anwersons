from fastapi import APIRouter, Request, Depends, Response
from fastapi import HTTPException
import typing as t

from app.db.session import get_db
from app.db.crud import (
    get_jobs,
    get_job,
    create_job,
    delete_job,
    edit_job,
)
from app.db.schemas import JobCreate, JobEdit, Job

job_router = r = APIRouter()

@r.get(
    "/jobs",
    response_model=t.List[Job],
    response_model_exclude_none=True,
)
async def jobs_list(
    response: Response,
    db=Depends(get_db),
):
    # Get all jobs
    jobs = get_jobs(db)
    response.headers["Content-Range"] = f"0-9/{len(jobs)}"
    return jobs


@r.get("/jobs/{job_id}", response_model=Job, response_model_exclude_none=True)
async def job_details(
    request: Request,
    job_id: int,
    db=Depends(get_db),
):
    # Get job details by ID
    job = get_job(db, job_id)
    return job


@r.post("/jobs", response_model=Job, response_model_exclude_none=True)
async def job_create(
    request: Request,
    job: JobCreate,
    db=Depends(get_db),
):
    # Create a new job
    try : 
        return create_job(db, job)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@r.put(
    "/jobs/{job_id}", response_model=Job, response_model_exclude_none=True
)
async def job_edit(
    request: Request,
    job_id: int,
    job: JobEdit,
    db=Depends(get_db),
):
    # Update existing job
    return edit_job(db, job_id, job)


@r.delete(
    "/jobs/{job_id}", response_model=Job, response_model_exclude_none=True
)
async def job_delete(
    request: Request,
    job_id: int,
    db=Depends(get_db),
):
    # Delete existing job
    return delete_job(db, job_id)