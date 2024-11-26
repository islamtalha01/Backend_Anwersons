import os
import sys
from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import lists, tickets, projects, attachments, issues, project_issues  # Import the new routers
from database.db import engine
from database.models import Base
from fastapi.responses import RedirectResponse, JSONResponse, StreamingResponse
import requests
from urllib.parse import urlparse
import base64

# Get the current script's directory
current_script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the project root path
project_root = os.path.abspath(os.path.join(current_script_directory, os.pardir))

# Append the project root and current script directory to the system path
sys.path.append(project_root)
sys.path.append(current_script_directory)

# Define allowed origins, methods, and headers
origins = [
    "*",
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

def valid_url(url: str = Query(...)):
    """
    Dependency to validate the URL query parameter.
    """
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise HTTPException(status_code=400, detail=f"Invalid URL specified: {url}")
    return url


@app.get("/proxy-url")
async def proxy_request(
    url: str = Depends(valid_url),
    response_type: str = Query("text", enum=["text", "blob"]),
):
    """
    Proxy endpoint to fetch data from the specified URL.
    """
    try:
        if response_type == "blob":
            # Stream the response directly
            resp = requests.get(url, stream=True)
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail="Failed to fetch data.")
            return StreamingResponse(resp.raw, media_type=resp.headers.get("Content-Type"))
        else:  # Default to 'text'
            resp = requests.get(url, stream=True)
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail="Failed to fetch data.")
            content_type = resp.headers.get("Content-Type")
            body = resp.content
            base64_data = f"data:{content_type};base64,{base64.b64encode(body).decode('utf-8')}"
            return JSONResponse({"data": base64_data})
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


# Include the routers for tasks, cards, lists, and issues
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(lists.router, prefix="/api/projects", tags=["Lists"])
app.include_router(tickets.router, prefix="", tags=["Tickets"])
app.include_router(attachments.router, prefix="/api/attachments", tags=["attachments"])
app.include_router(project_issues.router, prefix="/api/project-issues", tags=["project-issues"])
app.include_router(issues.router, prefix="/api/issues", tags=["issues"])

#updated app version for heroku

