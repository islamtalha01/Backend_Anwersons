from fastapi import APIRouter, HTTPException, Depends
from typing import List
from supabase import create_client
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import List as ListModel, Project, Ticket
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from schemas.list_schemas import ListCreate, ListResponse, ListsResponse, ListReorderRequest

router = APIRouter()
load_dotenv()

# Create Supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


@router.post("/{project_id}/lists", response_model=ListResponse)
async def create_list(project_id: int, list_data: ListCreate, db: Session = Depends(get_db)):
    # Fetch existing lists to determine the position
    existing_lists = db.query(ListModel).filter(ListModel.project_id == project_id).all()
    
    if existing_lists:
        # Determine the highest position and assign the next position
        positions = [list_item.position for list_item in existing_lists]
        position = max(positions) + 1
    else:
        # If no lists exist, set position to 0
        position = 0

    # Create a new list with the calculated position
    new_list = ListModel(
        name=list_data.name,
        project_id=project_id,
        position=position,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    try:
        # Insert the new list into the database
        db.add(new_list)
        db.commit()
        db.refresh(new_list)  # Refresh to get the new list's ID and other fields

        return new_list
    except Exception as e:
        db.rollback()  # Rollback in case of an error
        print(e)  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Error creating list")

# @router.post("/{project_id}/lists", response_model=ListResponse)
# async def create_list(list_data: ListCreate):
#     # Fetch existing lists to determine the position
#     lists_response = supabase.table("lists").select("position").execute()
    
#     if lists_response.data:
#         # Determine the highest position and assign the next position
#         positions = [list_item["position"] for list_item in lists_response.data]
#         position = max(positions) + 1
#     else:
#         # If no lists exist, set position to 0
#         position = 0

#     # Prepare the new list data with the calculated position
#     list_all_data = list_data.model_dump()
#     list_all_data["created_at"] = str(datetime.now(timezone.utc))
#     list_all_data["updated_at"] = str(datetime.now(timezone.utc))
#     list_all_data["position"] = position

#     # Insert the new list into the database
#     response = supabase.table("lists").insert(list_all_data).execute()
#     if response and response.data:
#         return response.data[0]
#     else:
#         raise HTTPException(status_code=400, detail="Error creating list")




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
async def get_lists_of_project(project_id: int, db: Session = Depends(get_db)):
    # Fetch the lists associated with the project
    project_lists = db.query(ListModel).filter(ListModel.project_id == project_id).all()

    if project_lists:
        return {"lists": project_lists}
    else:
        raise HTTPException(status_code=404, detail="Lists not found")

# @router.get("/{project_id}/lists", response_model=ListsResponse)
# async def get_lists_of_project(project_id: str):
#     response = supabase.table("lists").select("*").eq("project_id", project_id).execute()
#     if response.data:
#         return {"lists":response.data}
#     else:
#         raise HTTPException(status_code=404, detail="Lists not found")

@router.put("/{project_id}/lists/{list_id}", response_model=ListResponse)
async def update_list(project_id: int, list_id: int, list_data: ListCreate, db: Session = Depends(get_db)):
    # Fetch the list by ID and project_id
    db_list = db.query(ListModel).filter(ListModel.id == list_id, ListModel.project_id == project_id).first()

    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")

    # Update the list fields
    db_list.name = list_data.name
    db_list.project_id = list_data.project_id
    db_list.updated_at = datetime.now(timezone.utc)

    try:
        # Commit the changes to the database
        db.commit()
        db.refresh(db_list)  # Refresh to get the updated fields

        return db_list
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        print(e)  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Error updating list")

# @router.put("/{project_id}/lists/{list_id}", response_model=ListResponse)
# async def update_list(list_id: str, list_data: ListCreate):
#     list_all_data = list_data.model_dump()
#     list_all_data["updated_at"] = str(datetime.now(timezone.utc))
#     response = supabase.table("lists").update(list_all_data).eq("id", list_id).execute()
#     if response.data:
#         return response.data[0]
#     else:
#         return []


@router.delete("/{project_id}/lists/{list_id}")
async def delete_list(project_id: int, list_id: int, db: Session = Depends(get_db)):
    # Fetch the list by ID and project_id
    db_list = db.query(ListModel).filter(ListModel.id == list_id, ListModel.project_id == project_id).first()

    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")

    try:
        # Delete the list from the database
        db.delete(db_list)
        db.commit()

        # Reorder the remaining lists
        remaining_lists = (
            db.query(ListModel)
            .filter(ListModel.project_id == project_id)
            .order_by(ListModel.position)
            .all()
        )

        for index, list_item in enumerate(remaining_lists):
            list_item.position = index  # Adjust position
            db.add(list_item)  # Mark list as updated

        db.commit()  # Commit position updates

        return {"message": "List deleted and remaining lists reordered successfully"}
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        print(e)  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Error deleting list")

# @router.delete("/{project_id}/lists/{list_id}")
# async def delete_list(list_id: str):
#     response = supabase.table("lists").delete().eq("id", list_id).execute()
#     if response.data:
#         return {"message": "List deleted successfully"}
#     else:
#         raise HTTPException(status_code=404, detail="List not found")
    

@router.patch("/{project_id}/lists/reorder", response_model=ListsResponse)
async def reorder_lists(project_id: int, reorder_request: ListReorderRequest, db: Session = Depends(get_db)):
    """
    Reorder lists dynamically. Adjusts all positions starting from 0 after updating the list.
    """
    # Extract the list to reorder
    reordered_list = reorder_request.lists[0]  # Assuming only one list is being reordered

    # Fetch all lists for the given project
    existing_lists = db.query(ListModel).filter(ListModel.project_id == project_id).order_by(ListModel.position).all()

    if not existing_lists:
        raise HTTPException(status_code=404, detail="No lists found for the given project")

    # Find the target list
    target_list = next((l for l in existing_lists if l.id == reordered_list.id), None)
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
    try:
        for index, list_item in enumerate(updated_lists):
            list_item.position = index
            list_item.updated_at = datetime.now(timezone.utc)
            db.add(list_item)  # Add the updated list back to the session

        # Commit all changes to the database
        db.commit()
    except Exception as e:
        db.rollback()  # Rollback changes in case of an error
        print(e)  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Error updating list positions")

    # Fetch updated lists to ensure consistency
    final_lists = db.query(ListModel).filter(ListModel.project_id == project_id).order_by(ListModel.position).all()

    if final_lists:
        return {"lists": final_lists}
    else:
        raise HTTPException(status_code=400, detail="Error fetching updated lists")


# @router.patch("/{project_id}/lists/reorder", response_model=ListsResponse)
# async def reorder_lists(project_id: str, reorder_request: ListReorderRequest):
#     """
#     Reorder lists dynamically. Adjusts all positions starting from 0 after updating the list.
#     """
#     # Extract the list to reorder
#     reordered_list = reorder_request.lists[0]  # Assuming only one list is being reordered

#     # Fetch all lists for the given project
#     lists_response = supabase.table("lists").select("*").eq("project_id", project_id).order("position").execute()

#     if not lists_response.data:
#         raise HTTPException(status_code=404, detail="No lists found for the given project")

#     # Extract existing lists sorted by position
#     existing_lists = lists_response.data

#     # Find the list to reorder
#     target_list = next((l for l in existing_lists if l["id"] == reordered_list.id), None)
#     if not target_list:
#         raise HTTPException(status_code=400, detail=f"List with ID {reordered_list.id} does not exist in the project")

#     # Remove the target list from the list and insert it into the new position
#     existing_lists.remove(target_list)
#     new_position = reordered_list.position

#     updated_lists = (
#         existing_lists[:new_position]
#         + [target_list]
#         + existing_lists[new_position:]
#     )

#     # Assign new positions starting from 0
#     for index, list_item in enumerate(updated_lists):
#         list_item["position"] = index
#         list_item["updated_at"] = str(datetime.now(timezone.utc))

#     # Update the database with new positions
#     for list_item in updated_lists:
#         update_response = supabase.table("lists").update({
#             "position": list_item["position"],
#             "updated_at": list_item["updated_at"]
#         }).eq("id", list_item["id"]).execute()

#         if not update_response.data:
#             raise HTTPException(status_code=500, detail=f"Failed to update position for list with ID {list_item['id']}")

#     # Fetch updated lists to ensure consistency
#     final_lists_response = supabase.table("lists").select("*").eq("project_id", project_id).order("position").execute()

#     if final_lists_response.data:
#         return {"lists": final_lists_response.data}
#     else:
#         raise HTTPException(status_code=400, detail="Error fetching updated lists")


