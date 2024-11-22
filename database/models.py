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
    user_id = Column(Integer, nullable=False)

    # One-to-many relationship with Ticket and Issues
    tickets = relationship("Ticket", back_populates="project")
    issues = relationship("Issue", back_populates="project")


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
    
    
class SeverityEnum(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)  # Issue title
    description = Column(String, nullable=True)  # Detailed description of the issue
    steps_to_reproduce = Column(String, nullable=True)  # Steps to reproduce the issue
    expected_behaviour = Column(String, nullable=True)  # What was expected to happen
    actual_behaviour = Column(String, nullable=True)  # What actually happened
    severity = Column(Enum(SeverityEnum), nullable=False, default=SeverityEnum.medium)  # Severity level
    issue_metadata = Column(JSON, nullable=True)  # Additional data stored as JSON
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)  # Foreign key to Project
    image_id = Column(String, nullable=True)  # Reference to an image ID
    image_url = Column(String, nullable=True)  # URL of the associated image
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationship with Project
    project = relationship("Project", back_populates="issues")


