import os
import sys
from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import lists, tickets, projects, attachments, issues, project_issues
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
):
    """
    Proxy endpoint to stream content as it loads (progressive streaming).
    """
    try:
        # Stream the response from the target URL
        resp = requests.get(url, stream=True)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to fetch data.")

        content_type = resp.headers.get("Content-Type", "")
        
        # If the content is HTML, we stream it progressively
        if "text/html" in content_type:
            async def stream_html():
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        yield chunk  # Streaming the HTML in chunks as it's received

            return StreamingResponse(stream_html(), media_type="text/html")

        elif "application/javascript" in content_type or "text/css" in content_type:
            # For JS or CSS files, we stream them as well
            return StreamingResponse(resp.raw, media_type=content_type)

        elif "image" in content_type:
            # For images, stream them as-is
            return StreamingResponse(resp.raw, media_type=content_type)
        
        else:
            # For other types, stream the raw content
            return StreamingResponse(resp.raw, media_type=content_type)

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


# Include the routers for tasks, cards, lists, and issues
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(lists.router, prefix="/api/projects", tags=["Lists"])
app.include_router(tickets.router, prefix="", tags=["Tickets"])
app.include_router(attachments.router, prefix="/api/attachments", tags=["attachments"])
app.include_router(project_issues.router, prefix="/api/project-issues", tags=["project-issues"])
app.include_router(issues.router, prefix="/api/issues", tags=["issues"])
