# from sqlalchemy import Boolean, Column, Integer, String,Float,DateTime,func

# from .session import Base

# # user model
# class User(Base):
#     __tablename__ = "user"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     first_name = Column(String)
#     last_name = Column(String)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, default=True)
#     is_superuser = Column(Boolean, default=False)

# #model for the settings    
# class Setting(Base):
#     __tablename__ = "settings"
#     id = Column(Integer, primary_key=True, index=True)
#     key = Column(String, unique=True, index=True)
#     value = Column(String)


# #model for Agent
# class Agent(Base):
#     __tablename__ = "agents"
#     id = Column(Integer, primary_key=True, index=True)
#     date_created = Column(DateTime,default=func.now())
#     name = Column(String, index=True)
#     model_name = Column(String, index=True)
#     key = Column(String, index=True)
#     temperature = Column(Float, index=True) 
#     prompt = Column(String)
#     status = Column(Boolean, default=True)


