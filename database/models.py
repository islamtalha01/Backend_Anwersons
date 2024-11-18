from sqlalchemy import (
    Column, Integer, String, ForeignKey, TIMESTAMP, Boolean, Enum, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
import enum

Base = declarative_base()

class StatusEnum(enum.Enum):
    new = "new"
    pending = "pending"
    completed = "completed"

class PriorityEnum(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    position = Column(Integer, nullable=True)  # Represents the position of the list in the UI
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    members = Column(JSON, nullable=True)  # Store member usernames or IDs as a JSON array
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # One-to-many relationship with Ticket
    tickets = relationship("Ticket", back_populates="project")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    position = Column(Integer, nullable=False)  # Represents the position of the ticket in its list
    list_id = Column(Integer, ForeignKey("lists.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assignee = Column(String, nullable=True)  # The user assigned to the ticket
    priority = Column(Enum(PriorityEnum), nullable=True, default=PriorityEnum.medium)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.new)
    due_date = Column(TIMESTAMP, nullable=True)
    labels = Column(JSON, nullable=True)  # Store labels as an array of strings in JSON
    edit_mode = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Link to the project it belongs to
    project = relationship("Project", back_populates="tickets")
    
    
    