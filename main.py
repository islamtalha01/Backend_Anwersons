import os
import sys
from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import jobs
from database.db import engine
from database.models import Base
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse
import requests
from urllib.parse import urlparse

# Get the current script's directory
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the project root path
project_root = os.path.abspath(os.path.join(current_script_directory, os.pardir))

# Append the project root and current script directory to the system path
sys.path.append(project_root)
sys.path.append(current_script_directory)

# Define allowed origins, methods, and headers
origins = ["*"]

app = FastAPI(title="Backend", description="RESTful APIs")
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

def valid_url(url: str = Query(...)):
    """
    Dependency to validate the URL query parameter.
    """
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise HTTPException(status_code=400, detail=f"Invalid URL specified: {url}")
    return url


# Include the routers for tasks, cards, lists, and issues
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
