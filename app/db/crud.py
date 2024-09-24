# from fastapi import HTTPException, status
# from sqlalchemy.orm import Session
# import typing as t
# from app.db.models import Setting
# from app.db.models import Agent
# from app.db.schemas import AgentUpdate,AgentCreate

# from . import models, schemas
# from app.core.security import get_password_hash
# from app.db.schemas import SettingUpdate

# def get_user(db: Session, user_id: int):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(
#     db: Session, skip: int = 0, limit: int = 100
# ) -> t.List[schemas.UserOut]:
#     return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     hashed_password = get_password_hash(user.password)
#     db_user = models.User(
#         first_name=user.first_name,
#         last_name=user.last_name,
#         email=user.email,
#         is_active=user.is_active,
#         is_superuser=user.is_superuser,
#         hashed_password=hashed_password,
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def delete_user(db: Session, user_id: int):
#     user = get_user(db, user_id)
#     if not user:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
#     db.delete(user)
#     db.commit()
#     return user


# def edit_user(
#     db: Session, user_id: int, user: schemas.UserEdit
# ) -> schemas.User:
#     db_user = get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
#     update_data = user.dict(exclude_unset=True)

#     if "password" in update_data:
#         update_data["hashed_password"] = get_password_hash(user.password)
#         del update_data["password"]

#     for key, value in update_data.items():
#         setattr(db_user, key, value)

#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# # crud for the settings
# def get_all_settings(db: Session):
#     return db.query(Setting).all()

# def get_setting(db: Session, key: str):
#     return db.query(Setting).filter(Setting.key == key).first()

# def update_setting(db: Session, key: str, setting: SettingUpdate):
#     db_setting = db.query(Setting).filter(Setting.key == key).first()
#     if db_setting:
#         db_setting.value = setting.value
#         db.commit()
#         db.refresh(db_setting)
#         return db_setting
#     return None

# def delete_setting(db: Session, key: str):
#     db_setting = db.query(Setting).filter(Setting.key == key).first()
#     if db_setting:
#         db.delete(db_setting)
#         db.commit()
#         return db_setting
#     return None

# #crud for agents
# def create_agent(db: Session, agent: AgentCreate):
#     db_agent = Agent(**agent.dict())
#     db.add(db_agent)
#     db.commit()
#     db.refresh(db_agent)
#     return db_agent

# def update_agent(db: Session, agent_id: int, agent: AgentUpdate):
#     db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
#     if db_agent:
#         for key, value in agent.dict().items():
#             setattr(db_agent, key, value)
#         db.commit()
#         db.refresh(db_agent)
#         return db_agent
#     else:
#         db_agent = Agent(**agent.dict())
#         db.add(db_agent)
#         db.commit()
#         db.refresh(db_agent)
#         return db_agent

# def get_agent(db: Session, agent_id: int):
#     return db.query(Agent).filter(Agent.id == agent_id).first()

# def get_agents(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(Agent).offset(skip).limit(limit).all()

# def delete_agent(db: Session, agent_id: int):
#     db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
#     if db_agent:
#         db.delete(db_agent)
#         db.commit()
#         return db_agent
#     return None

# def detail_agent(db: Session,agent_id: int):
#     agent = db.query(Agent).filter(Agent.id == agent_id).first()
#     if not agent:
#         raise HTTPException(status_code=404, detail="Agent not found")
#     return agent
