from fastapi import APIRouter, HTTPException
from typing import List
from supabase import create_client
import os
from datetime import datetime, timezone
from schemas.project_schemas import ProjectCreate, ProjectResponse, ProjectDetailResponse

router = APIRouter()

# Create Supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# CRUD API endpoints for Project

@router.post("/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate):
    project_data = project.model_dump()
    project_data["created_at"] = str(datetime.now(timezone.utc))
    project_data["updated_at"] = str(datetime.now(timezone.utc))
    
    response = supabase.table("projects").insert(project_data).execute()
    if response.data:
        return response.data[0]
    else:
        raise HTTPException(status_code=400, detail="Error creating project")

@router.get("/", response_model=List[ProjectResponse])
async def get_projects():
    response = supabase.table("projects").select("*").execute()
    if response.data:
        return response.data
    else:
        raise HTTPException(status_code=400, detail="Error fetching projects")


@router.get("/{project_id}", response_model=ProjectDetailResponse)
async def get_project_with_lists_and_tickets(project_id: int):
    # Fetch the project
    project_response = supabase.table("projects").select("*").eq("id", project_id).execute()
    if not project_response.data:
        raise HTTPException(status_code=404, detail="Project not found")
    project = project_response.data[0]

    # Fetch the lists associated with the project
    lists_response = supabase.table("lists").select("*").eq("project_id", project_id).execute()
    if not lists_response.data:
        lists_response.data = []  # If no lists, return an empty array
    project_lists = lists_response.data

    # Fetch tickets for each list and map them to their respective lists
    lists_with_tickets = []
    for list_item in project_lists:
        tickets_response = supabase.table("tickets").select("*").eq("list_id", list_item["id"]).execute()
        tickets = tickets_response.data if tickets_response.data else []
        lists_with_tickets.append({
            **list_item,
            "tickets": tickets
        })

    # Construct the response
    return {
        "id": project["id"],
        "name": project["name"],
        "description": project["description"],
        "lists": lists_with_tickets
    }

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project: ProjectCreate):
    project_data = project.model_dump()
    project_data["updated_at"] = str(datetime.now(timezone.utc))  # Update the updated timestamp
    response = supabase.table("projects").update(project_data).eq("id", project_id).execute()
    if response.data:
        return response.data[0]
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@router.delete("/{project_id}")
async def delete_project(project_id: int):
    response = supabase.table("projects").delete().eq("id", project_id).execute()
    if response.data:
        return {"message": "Project deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Project not found")

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