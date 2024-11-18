from fastapi import APIRouter, HTTPException, Depends
from typing import List
from supabase import create_client
import os
from datetime import datetime, timezone
from schemas.ticket_schemas import TicketCreate, TicketResponse, TicketReorderRequest, TicketReorderItem

router = APIRouter()

# Create Supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

async def project_exists(project_id: str):
    response = supabase.table("projects").select("*").eq("id", project_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Project not found")
    return response.data[0]

async def list_exists(list_id: str, project_id: str):
    response = supabase.table("lists").select("*").eq("id", list_id).eq("project_id", project_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="List not found")
    return response.data[0]

async def ticket_exists(ticket_id: str):
    response = supabase.table("tickets").select("*").eq("id", ticket_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return response.data[0]


@router.post("/api/projects/{project_id}/lists/{list_id}/tickets", response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate):
    ticket_data = ticket.model_dump()
    
    # Validate project and list exist
    await project_exists(ticket.project_id)
    await list_exists(ticket.list_id, ticket.project_id)
    
    # Fetch tickets for the specified list to determine the position
    list_tickets_response = supabase.table("tickets").select("position").eq("list_id", ticket.list_id).execute()
    
    if not list_tickets_response.data:
        # If no tickets exist in the list, set position to 0
        position = 0
    else:
        # Determine the highest position and assign the next position
        positions = [ticket["position"] for ticket in list_tickets_response.data]
        position = max(positions) + 1

    # Prepare ticket data with calculated position
    ticket_data = ticket.model_dump()
    ticket_data["created_at"] = str(datetime.now(timezone.utc))
    ticket_data["updated_at"] = str(datetime.now(timezone.utc))
    ticket_data["due_date"] = str(ticket_data["due_date"])
    ticket_data["position"] = position

    # Insert the new ticket into the database
    response = supabase.table("tickets").insert(ticket_data).execute()
    if response and response.data:
        return response.data[0]
    else:
        raise HTTPException(status_code=400, detail="Error creating ticket")



@router.get("/api/projects/{project_id}/lists/{list_id}/tickets", response_model=List[TicketResponse])
async def get_tickets_of_list(list_id: str, project_id: str):
    # validate project and list exist
    await project_exists(project_id)
    await list_exists(list_id, project_id)
    
    response = supabase.table("tickets").select("*").eq("list_id", list_id).eq("project_id", project_id).execute()
    if response.data:
        return response.data
    else:
        raise HTTPException(status_code=404, detail="Ticket not found")

@router.put("/api/projects/{project_id}/lists/{list_id}/tickets/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: str, ticket: TicketCreate):
    
    ticket_data = ticket.model_dump()
    ticket_data["updated_at"] = str(datetime.now(timezone.utc))
    ticket_data["due_date"] = str(ticket_data["due_date"])
    response = supabase.table("tickets").update(ticket_data).eq("id", ticket_id).execute()
    
    if response.data:
        return response.data[0]
    else:
        raise HTTPException(status_code=404, detail="Ticket not found")


@router.delete("/api/projects/{project_id}/lists/{list_id}/tickets/{ticket_id}")
async def delete_ticket(ticket_id: str, project_id: str, list_id: str):
    # Validate project, list, and ticket exist
    await project_exists(project_id)
    await list_exists(list_id, project_id)
    await ticket_exists(ticket_id)

    # Delete the ticket
    response = supabase.table("tickets").delete().eq("id", ticket_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Fetch remaining tickets in the list, ordered by position
    remaining_tickets_response = (
        supabase.table("tickets")
        .select("*")
        .eq("list_id", list_id)
        .eq("project_id", project_id)
        .order("position")
        .execute()
    )
    remaining_tickets = remaining_tickets_response.data if remaining_tickets_response.data else []

    # Reassign positions for the remaining tickets
    updated_tickets = [
        {
            **ticket,
            "position": index,
            "updated_at": str(datetime.now(timezone.utc)),
        }
        for index, ticket in enumerate(remaining_tickets)
    ]

    # Update the database with the new positions
    for ticket in updated_tickets:
        supabase.table("tickets").update({
            "position": ticket["position"],
            "updated_at": ticket["updated_at"]
        }).eq("id", ticket["id"]).execute()

    return {"message": "Ticket deleted and remaining tickets reordered successfully"}



@router.patch("/{project_id}/tickets/reorder", response_model=TicketReorderRequest)
async def reorder_tickets(project_id: str, reorder_request: TicketReorderRequest):
    """
    Reorder tickets dynamically within the same list or move to a different list.
    Adjust positions for both source and destination lists.
    """
    # Extract the ticket to reorder
    reordered_ticket = reorder_request.tickets[0]  # Assuming only one ticket is being reordered

    # Fetch tickets from the source list
    source_tickets_response = (
        supabase.table("tickets")
        .select("*")
        .eq("project_id", project_id)
        .eq("list_id", reordered_ticket.source_list_id)
        .order("position")
        .execute()
    )
    source_tickets = source_tickets_response.data if source_tickets_response.data else []

    # Fetch tickets from the destination list
    destination_tickets_response = (
        supabase.table("tickets")
        .select("*")
        .eq("project_id", project_id)
        .eq("list_id", reordered_ticket.destination_list_id)
        .order("position")
        .execute()
    )
    destination_tickets = destination_tickets_response.data if destination_tickets_response.data else []

    # Remove the ticket from the source list and reassign positions
    updated_source_tickets = [
        {
            **ticket,
            "position": index,
            "updated_at": str(datetime.now(timezone.utc)),
        }
        for index, ticket in enumerate(ticket for ticket in source_tickets if ticket["id"] != reordered_ticket.id)
    ]

    # Update source list in the database
    for ticket in updated_source_tickets:
        supabase.table("tickets").update({
            "position": ticket["position"],
            "updated_at": ticket["updated_at"]
        }).eq("id", ticket["id"]).execute()

    # Insert the ticket into the destination list at the specified position
    destination_tickets.insert(reordered_ticket.position, {
        "id": reordered_ticket.id,
        "list_id": reordered_ticket.destination_list_id,
    })

    # Reassign positions for the destination list
    updated_destination_tickets = [
        {
            **ticket,
            "position": index,
            "updated_at": str(datetime.now(timezone.utc)),
        }
        for index, ticket in enumerate(destination_tickets)
    ]

    # Update destination list in the database
    for ticket in updated_destination_tickets:
        supabase.table("tickets").update({
            "position": ticket["position"],
            "updated_at": ticket["updated_at"],
            "list_id": ticket.get("list_id", reordered_ticket.destination_list_id)
        }).eq("id", ticket["id"]).execute()

    # Update the moved ticket's list ID
    supabase.table("tickets").update({
        "list_id": reordered_ticket.destination_list_id,
        "position": reordered_ticket.position,
        "updated_at": str(datetime.now(timezone.utc))
    }).eq("id", reordered_ticket.id).execute()

    # Prepare the response
    serialized_tickets = [
        TicketReorderItem(
            id=reordered_ticket.id,
            source_list_id=reordered_ticket.source_list_id,
            destination_list_id=reordered_ticket.destination_list_id,
            position=reordered_ticket.position
        )
    ]

    return {"tickets": serialized_tickets}




