import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import lists, tickets, projects  # Import the new routers
from database.db import engine
from database.models import Base
from fastapi.responses import RedirectResponse
# Get the current script's directory
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the project root path
project_root = os.path.abspath(os.path.join(current_script_directory, os.pardir))

# Append the project root and current script directory to the system path
sys.path.append(project_root)
sys.path.append(current_script_directory)

# Define allowed origins, methods, and headers
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
]

app = FastAPI(title="mini-kanban-backend", description="RESTful APIs")
Base.metadata.create_all(bind=engine) 

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic Hello World endpoint for testing
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


# Include the routers for tasks, cards, lists, and issues
app.include_router(tickets.router, prefix="", tags=["Tickets"])
app.include_router(lists.router, prefix="/api/projects", tags=["Lists"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
