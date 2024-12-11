import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import jobs, customers
from database.db import engine
from database.models import Base
from fastapi.responses import RedirectResponse
#import requests



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


# Include the routers for tasks, cards, lists, and issues
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])

app.include_router(customers.router, prefix="/api/v1", tags=["Customers"])