from fastapi import APIRouter, HTTPException
from typing import List
from supabase import create_client
import os
from datetime import datetime, timezone
from schemas.list_schemas import ListCreate, ListResponse, ListsResponse, ListReorderRequest

router = APIRouter()

# Create Supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


@router.post("/{project_id}/lists", response_model=ListResponse)
async def create_list(list_data: ListCreate):
    # Fetch existing lists to determine the position
    lists_response = supabase.table("lists").select("position").execute()
    
    if lists_response.data:
        # Determine the highest position and assign the next position
        positions = [list_item["position"] for list_item in lists_response.data]
        position = max(positions) + 1
    else:
        # If no lists exist, set position to 0
        position = 0

    # Prepare the new list data with the calculated position
    list_all_data = list_data.model_dump()
    list_all_data["created_at"] = str(datetime.now(timezone.utc))
    list_all_data["updated_at"] = str(datetime.now(timezone.utc))
    list_all_data["position"] = position

    # Insert the new list into the database
    response = supabase.table("lists").insert(list_all_data).execute()
    if response and response.data:
        return response.data[0]
    else:
        raise HTTPException(status_code=400, detail="Error creating list")




# @router.post("/", response_model=ListResponse)
# async def create_list(list_data: ListCreate):
    
#     list_all_data = list_data.model_dump()
#     list_all_data["created_at"] = str(datetime.now(timezone.utc))
#     list_all_data["updated_at"] = str(datetime.now(timezone.utc))
    
#     response = supabase.table("lists").insert(list_all_data).execute()
#     if response:
#         return response.data[0]
#     else:
#         raise HTTPException(status_code=400, detail="Error creating list")

# @router.get("/", response_model=List[ListResponse])
# async def get_lists():
#     response = supabase.table("lists").select("*").execute()
#     if response.data:
#         return response.data
#     else:
#         raise HTTPException(status_code=400, detail="Error fetching lists")

@router.get("/{project_id}/lists", response_model=ListsResponse)
async def get_lists_of_project(project_id: str):
    response = supabase.table("lists").select("*").eq("project_id", project_id).execute()
    if response.data:
        return {"lists":response.data}
    else:
        raise HTTPException(status_code=404, detail="Lists not found")

@router.put("/{project_id}/lists/{list_id}", response_model=ListResponse)
async def update_list(list_id: str, list_data: ListCreate):
    list_all_data = list_data.model_dump()
    list_all_data["updated_at"] = str(datetime.now(timezone.utc))
    response = supabase.table("lists").update(list_all_data).eq("id", list_id).execute()
    if response.data:
        return response.data[0]
    else:
        raise HTTPException(status_code=404, detail="List not found")

@router.delete("/{project_id}/lists/{list_id}")
async def delete_list(list_id: str):
    response = supabase.table("lists").delete().eq("id", list_id).execute()
    if response.data:
        return {"message": "List deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="List not found")
    

@router.patch("/{project_id}/lists/reorder", response_model=ListsResponse)
async def reorder_lists(project_id: str, reorder_request: ListReorderRequest):
    """
    Reorder lists dynamically. Adjusts all positions starting from 0 after updating the list.
    """
    # Extract the list to reorder
    reordered_list = reorder_request.lists[0]  # Assuming only one list is being reordered

    # Fetch all lists for the given project
    lists_response = supabase.table("lists").select("*").eq("project_id", project_id).order("position").execute()

    if not lists_response.data:
        raise HTTPException(status_code=404, detail="No lists found for the given project")

    # Extract existing lists sorted by position
    existing_lists = lists_response.data

    # Find the list to reorder
    target_list = next((l for l in existing_lists if l["id"] == reordered_list.id), None)
    if not target_list:
        raise HTTPException(status_code=400, detail=f"List with ID {reordered_list.id} does not exist in the project")

    # Remove the target list from the list and insert it into the new position
    existing_lists.remove(target_list)
    new_position = reordered_list.position

    updated_lists = (
        existing_lists[:new_position]
        + [target_list]
        + existing_lists[new_position:]
    )

    # Assign new positions starting from 0
    for index, list_item in enumerate(updated_lists):
        list_item["position"] = index
        list_item["updated_at"] = str(datetime.now(timezone.utc))

    # Update the database with new positions
    for list_item in updated_lists:
        update_response = supabase.table("lists").update({
            "position": list_item["position"],
            "updated_at": list_item["updated_at"]
        }).eq("id", list_item["id"]).execute()

        if not update_response.data:
            raise HTTPException(status_code=500, detail=f"Failed to update position for list with ID {list_item['id']}")

    # Fetch updated lists to ensure consistency
    final_lists_response = supabase.table("lists").select("*").eq("project_id", project_id).order("position").execute()

    if final_lists_response.data:
        return {"lists": final_lists_response.data}
    else:
        raise HTTPException(status_code=400, detail="Error fetching updated lists")


