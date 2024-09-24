# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db import models

# from fastapi import APIRouter, Depends, Response,Request, HTTPException
# import typing as t
# from sqlalchemy.orm import Session
# from app.db.models import Agent  # Import the Setting model here

# from app.db.session import get_db,engine

# from app.db.crud import (
#     create_agent,
#     update_agent,
#     get_agent,
#     get_agents,
#     delete_agent,
#     detail_agent
# )
# from app.db.schemas import  AgentCreate, AgentUpdate, Agent


# agents_router = r = APIRouter()

# models.Base.metadata.create_all(bind=engine)

# @r.post("/agent", response_model=Agent)
# def agent_create(agent: AgentCreate, db: Session = Depends(get_db)):
#     db_agent = create_agent(db, agent)
#     return db_agent

# @r.post("/agent/{agent_id}", response_model=Agent)
# def agent_update(agent_id: int, agent: AgentUpdate, db: Session = Depends(get_db)):
#     db_agent = update_agent(db, agent_id, agent)
#     return db_agent

# @r.get("/agent/{agent_id}", response_model=Agent)
# def read_agent(agent_id: int, db: Session = Depends(get_db)):
#     db_agent = get_agent(db, agent_id)
#     if db_agent is None:
#         raise HTTPException(status_code=404, detail="Agent not found")
#     return db_agent

# @r.get("/agents", response_model=list[Agent])
# def read_agents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     agents = get_agents(db, skip=skip, limit=limit)
#     return agents

# @r.delete("/agent/{agent_id}", response_model=Agent)
# def agent_delete(agent_id: int, db: Session = Depends(get_db)):
#     db_agent = delete_agent(db, agent_id)
#     if db_agent is None:
#         raise HTTPException(status_code=404, detail="Agent not found")
#     return db_agent

# @r.get("/agents/{agent_id}", response_model=Agent)
# def agent_detail(agent_id: int, db: Session = Depends(get_db)):
#     return detail_agent(db, agent_id)