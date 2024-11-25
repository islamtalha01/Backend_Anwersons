from fastapi import APIRouter, HTTPException, Depends
from typing import List
from supabase import create_client
import os
from datetime import datetime, timezone
from schemas.ticket_schemas import TicketCreate, TicketResponse, TicketReorderRequest, TicketReorderItem
from database.models import List as ListModel, Project, Ticket
from sqlalchemy.orm import Session
from database.db import get_db

router = APIRouter()

# Create Supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

async def project_exists(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

async def list_exists(list_id: int, project_id: int, db: Session = Depends(get_db)):
    list_item = db.query(ListModel).filter(ListModel.id == list_id, ListModel.project_id == project_id).first()
    if not list_item:
        raise HTTPException(status_code=404, detail="List not found")
    return list_item

async def ticket_exists(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket




@router.post("/api/projects/{project_id}/lists/{list_id}/tickets", response_model=TicketResponse)
async def create_ticket(
    project_id: int, 
    list_id: int, 
    ticket: TicketCreate, 
    db: Session = Depends(get_db)
):
    # Validate project and list exist
    await project_exists(project_id, db)
    await list_exists(list_id, project_id, db)

    # Fetch tickets for the specified list to determine the position
    list_tickets = db.query(Ticket).filter(Ticket.list_id == list_id).order_by(Ticket.position).all()

    if not list_tickets:
        # If no tickets exist in the list, set position to 0
        position = 0
    else:
        # Determine the highest position and assign the next position
        positions = [ticket.position for ticket in list_tickets]
        position = max(positions) + 1

    # Prepare ticket data with calculated position
    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        list_id=list_id,
        project_id=project_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        due_date=ticket.due_date,
        position=position,
        assignee=ticket.assignee,
        priority=ticket.priority,
        status = ticket.status,
        edit_mode=ticket.edit_mode,
        labels=ticket.labels
    )

    try:
        # Insert the new ticket into the database
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)  # Refresh to get the new ticket's ID and other fields

        return new_ticket
    except Exception as e:
        db.rollback()  # Rollback in case of an error
        print(e)  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Error creating ticket")



@router.get("/api/projects/{project_id}/lists/{list_id}/tickets", response_model=List[TicketResponse])
async def get_tickets_of_list(
    project_id: int, 
    list_id: int, 
    db: Session = Depends(get_db)
):
    # Validate project and list exist
    await project_exists(project_id, db)
    await list_exists(list_id, project_id, db)

    # Fetch tickets for the specified list
    tickets = db.query(Ticket).filter(Ticket.list_id == list_id, Ticket.project_id == project_id).all()

    if not tickets:
        return []

    return tickets



@router.put("/api/projects/{project_id}/lists/{list_id}/tickets/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    project_id: int, 
    list_id: int, 
    ticket_id: int, 
    ticket: TicketCreate, 
    db: Session = Depends(get_db)
):
    # Fetch the ticket by ID, list ID, and project ID
    db_ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id,
        Ticket.list_id == list_id,
        Ticket.project_id == project_id
    ).first()

    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Update the ticket fields
    db_ticket.title = ticket.title
    db_ticket.description = ticket.description
    db_ticket.due_date = ticket.due_date
    db_ticket.updated_at = datetime.now(timezone.utc)

    try:
        # Commit the changes to the database
        db.commit()
        db.refresh(db_ticket)  # Refresh to get the updated fields

        return db_ticket
    except Exception as e:
        db.rollback()  # Rollback in case of an error
        print(e)  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Error updating ticket")


@router.delete("/api/projects/{project_id}/lists/{list_id}/tickets/{ticket_id}")
async def delete_ticket(
    ticket_id: int, 
    project_id: int, 
    list_id: int, 
    db: Session = Depends(get_db)
):
    # Validate project, list, and ticket exist
    await project_exists(project_id, db)
    await list_exists(list_id, project_id, db)
    await ticket_exists(ticket_id, db)

    try:
        # Delete the ticket
        db_ticket = db.query(Ticket).filter(
            Ticket.id == ticket_id,
            Ticket.list_id == list_id,
            Ticket.project_id == project_id
        ).first()

        if not db_ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        db.delete(db_ticket)
        db.commit()

        # Fetch remaining tickets in the list, ordered by position
        remaining_tickets = db.query(Ticket).filter(
            Ticket.list_id == list_id,
            Ticket.project_id == project_id
        ).order_by(Ticket.position).all()

        # Reassign positions for the remaining tickets
        for index, ticket in enumerate(remaining_tickets):
            ticket.position = index
            ticket.updated_at = datetime.now(timezone.utc)
            db.add(ticket)  # Mark ticket for update

        db.commit()  # Commit the updated positions

        return {"message": "Ticket deleted and remaining tickets reordered successfully"}

    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        print(e)  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Error deleting ticket")



@router.patch("/{project_id}/tickets/reorder", response_model=TicketReorderRequest)
async def reorder_tickets(
    project_id: int,
    reorder_request: TicketReorderRequest,
    db: Session = Depends(get_db)
):
    """
    Reorder tickets dynamically within the same list or move to a different list.
    Adjust positions for both source and destination lists.
    """
    # Extract the ticket to reorder
    reordered_ticket = reorder_request.tickets[0]  # Assuming only one ticket is being reordered

    # Fetch the ticket to be moved
    moved_ticket = db.query(Ticket).filter(Ticket.id == reordered_ticket.id).first()
    if not moved_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Handle moving tickets across lists
    if reordered_ticket.source_list_id != reordered_ticket.destination_list_id:
        # Fetch tickets from the source list
        source_tickets = db.query(Ticket).filter(
            Ticket.project_id == project_id,
            Ticket.list_id == reordered_ticket.source_list_id
        ).order_by(Ticket.position).all()

        if not source_tickets:
            raise HTTPException(status_code=404, detail="No tickets found in the source list")

        # Fetch tickets from the destination list
        destination_tickets = db.query(Ticket).filter(
            Ticket.project_id == project_id,
            Ticket.list_id == reordered_ticket.destination_list_id
        ).order_by(Ticket.position).all()

        # Remove the ticket from the source list
        updated_source_tickets = [
            ticket for ticket in source_tickets if ticket.id != reordered_ticket.id
        ]

        # Reassign positions for the source list
        for index, ticket in enumerate(updated_source_tickets):
            ticket.position = index
            ticket.updated_at = datetime.now(timezone.utc)
            db.add(ticket)  # Mark for update

        # Update the ticket to move to the destination list
        moved_ticket.list_id = reordered_ticket.destination_list_id
        moved_ticket.position = reordered_ticket.position
        moved_ticket.updated_at = datetime.now(timezone.utc)

        # Insert the moved ticket into the destination list
        destination_tickets.insert(reordered_ticket.position, moved_ticket)

        # Reassign positions for the destination list
        for index, ticket in enumerate(destination_tickets):
            ticket.position = index
            ticket.updated_at = datetime.now(timezone.utc)
            db.add(ticket)  # Mark for update

    # Handle reordering tickets within the same list
    else:
        # Fetch tickets from the source/destination list (same list)
        tickets = db.query(Ticket).filter(
            Ticket.project_id == project_id,
            Ticket.list_id == reordered_ticket.source_list_id
        ).order_by(Ticket.position).all()

        if not tickets:
            raise HTTPException(status_code=404, detail="No tickets found in the list")

        # Remove the ticket from the list and reinsert it at the new position
        updated_tickets = [
            ticket for ticket in tickets if ticket.id != reordered_ticket.id
        ]
        updated_tickets.insert(reordered_ticket.position, moved_ticket)

        # Reassign positions for all tickets in the list
        for index, ticket in enumerate(updated_tickets):
            ticket.position = index
            ticket.updated_at = datetime.now(timezone.utc)
            db.add(ticket)  # Mark for update

    try:
        # Commit all changes
        db.commit()

        # Prepare the response
        serialized_tickets = [
            TicketReorderItem(
                id=ticket.id,
                source_list_id=reordered_ticket.source_list_id,
                destination_list_id=reordered_ticket.destination_list_id,
                position=ticket.position
            )
            for ticket in updated_tickets
        ] if reordered_ticket.source_list_id == reordered_ticket.destination_list_id else [
            TicketReorderItem(
                id=ticket.id,
                source_list_id=reordered_ticket.source_list_id,
                destination_list_id=reordered_ticket.destination_list_id,
                position=ticket.position
            )
            for ticket in destination_tickets
        ]

        return {"tickets": serialized_tickets}
    except Exception as e:
        db.rollback()
        print(e)  # Log the error
        raise HTTPException(status_code=500, detail="Error reordering tickets")





