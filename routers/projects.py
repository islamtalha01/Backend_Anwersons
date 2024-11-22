# from fastapi import APIRouter, HTTPException
# from typing import List
# from supabase import create_client
# import os
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db  # Database session dependency
from database.models import List as ListModel, Project, Ticket  # SQLAlchemy model for "projects"
from schemas.project_schemas import ProjectResponse  # Response schema for Project

from schemas.project_schemas import ProjectCreate, ProjectResponse, ProjectDetailResponse

router = APIRouter()

# Create Supabase client
# supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# CRUD API endpoints for Project

@router.post("/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        # Create a new Project instance
        new_project = Project(
            name=project.name,
            description=project.description,
            members=project.members,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            user_id = project.user_id
        )

        # Add the new project to the database
        db.add(new_project)
        db.commit()
        db.refresh(new_project)  # Refresh to get the new project's ID and other fields

        return new_project
    except Exception as e:
        print(e)  # Optional: Log the exception for debugging
        raise HTTPException(status_code=500, detail="Error creating project")

# @router.post("/", response_model=ProjectResponse)
# async def create_project(project: ProjectCreate):
#     project_data = project.model_dump()
#     project_data["created_at"] = str(datetime.now(timezone.utc))
#     project_data["updated_at"] = str(datetime.now(timezone.utc))
    
#     response = supabase.table("projects").insert(project_data).execute()
#     if response.data:
#         return response.data[0]
#     else:
#         raise HTTPException(status_code=400, detail="Error creating project")



@router.get("/", response_model=List[ProjectResponse])
async def get_projects(db: Session = Depends(get_db)):
    # Fetch all projects from the database
    projects = db.query(Project).all()
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found")
    return projects


# @router.get("/", response_model=List[ProjectResponse])
# async def get_projects():
#     response = supabase.table("projects").select("*").execute()
#     if response.data:
#         return response.data
#     else:
#         raise HTTPException(status_code=400, detail="Error fetching projects")


@router.get("/{project_id}", response_model=ProjectDetailResponse)
async def get_project_with_lists_and_tickets(project_id: int, db: Session = Depends(get_db)):
    # Fetch the project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Fetch the lists associated with the project
    project_lists = db.query(ListModel).filter(ListModel.project_id == project_id).all()

    # Fetch tickets for each list and map them to their respective lists
    lists_with_tickets = []
    for list_item in project_lists:
        tickets = db.query(Ticket).filter(Ticket.list_id == list_item.id).all()
        lists_with_tickets.append({
            "id": list_item.id,
            "name": list_item.name,
            "project_id": list_item.project_id,
            "position": list_item.position,
            "created_at": list_item.created_at,
            "updated_at": list_item.updated_at,
            "tickets": tickets
        })

    # Construct the response
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "lists": lists_with_tickets
    }



# @router.get("/{project_id}", response_model=ProjectDetailResponse)
# async def get_project_with_lists_and_tickets(project_id: int):
#     # Fetch the project
#     project_response = supabase.table("projects").select("*").eq("id", project_id).execute()
#     if not project_response.data:
#         raise HTTPException(status_code=404, detail="Project not found")
#     project = project_response.data[0]

#     # Fetch the lists associated with the project
#     lists_response = supabase.table("lists").select("*").eq("project_id", project_id).execute()
#     if not lists_response.data:
#         lists_response.data = []  # If no lists, return an empty array
#     project_lists = lists_response.data

#     # Fetch tickets for each list and map them to their respective lists
#     lists_with_tickets = []
#     for list_item in project_lists:
#         tickets_response = supabase.table("tickets").select("*").eq("list_id", list_item["id"]).execute()
#         tickets = tickets_response.data if tickets_response.data else []
#         lists_with_tickets.append({
#             **list_item,
#             "tickets": tickets
#         })

#     # Construct the response
#     return {
#         "id": project["id"],
#         "name": project["name"],
#         "description": project["description"],
#         "lists": lists_with_tickets
#     }

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    # Find the project by ID
    db_project = db.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Update the project fields
    db_project.name = project.name
    db_project.description = project.description
    db_project.members = project.members
    db_project.updated_at = datetime.now(timezone.utc)

    try:
        # Commit the changes to the database
        db.commit()
        db.refresh(db_project)  # Refresh to get the updated fields

        return db_project
    except Exception as e:
        db.rollback()  # Roll back the transaction in case of an error
        print(e)  # Log the exception for debugging
        raise HTTPException(status_code=500, detail="Error updating project")

# @router.put("/{project_id}", response_model=ProjectResponse)
# async def update_project(project_id: int, project: ProjectCreate):
#     project_data = project.model_dump()
#     project_data["updated_at"] = str(datetime.now(timezone.utc))  # Update the updated timestamp
#     response = supabase.table("projects").update(project_data).eq("id", project_id).execute()
#     if response.data:
#         return response.data[0]
#     else:
#         raise HTTPException(status_code=404, detail="Project not found")


@router.delete("/{project_id}")
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    # Delete related lists first
    lists_deleted = db.query(ListModel).filter(ListModel.project_id == project_id).delete()
    db.commit()  # Commit deletion of related lists

    # Delete the project
    project_deleted = db.query(Project).filter(Project.id == project_id).delete()
    db.commit()  # Commit deletion of the project

    if project_deleted:
        return {"message": "Project deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Project not found")

# @router.delete("/{project_id}")
# async def delete_project(project_id: int):
#     supabase.table("lists").delete().eq("project_id", project_id).execute()
#     response = supabase.table("projects").delete().eq("id", project_id).execute()
#     if response.data:
#         return {"message": "Project deleted successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="Project not found")

# @router.get("/{project_id}/lists", response_model=List[dict])
# async def get_project_lists(project_id: int):
#     response = supabase.table("lists").select("*").eq("project_id", project_id).execute()
#     if response.data:
#         return response.data
#     else:
#         raise HTTPException(status_code=404, detail="No lists found for the specified project")
    
    
# @router.get("/{project_id}/lists/{list_id}", response_model=dict)
# async def get_project_list(project_id: int, list_id: int):
#     response = supabase.table("lists").select("*").eq("project_id", project_id).eq("id", list_id).execute()
#     if response.data:
#         return response.data[0]
#     else:
#         raise HTTPException(status_code=404, detail="List not found for the specified project")
    
    
# @router.get("/projects/{project_id}/lists-tickets", response_model=dict)
# async def get_lists_and_tickets_for_project(project_id: int):
#     lists_response = supabase.table("lists").select("*").eq("project_id", project_id).execute()
#     if not lists_response.data:
#         raise HTTPException(status_code=404, detail="No lists found for the specified project")

#     lists_with_tickets = []
#     for list_item in lists_response.data:
#         tickets_response = supabase.table("tickets").select("*").eq("list_id", list_item["id"]).execute()
#         list_item["tickets"] = tickets_response.data if tickets_response.data else []
#         lists_with_tickets.append(list_item)

#     return {"project_id": project_id, "lists": lists_with_tickets}