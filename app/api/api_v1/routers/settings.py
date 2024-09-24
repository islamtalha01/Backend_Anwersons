

# from fastapi import APIRouter, Depends, Response,Request, HTTPException
# import typing as t
# from sqlalchemy.orm import Session
# from app.db.models import Setting  # Import the Setting model here

# from app.db.session import get_db

# from app.db.crud import (
#     get_all_settings,
#     get_setting,
#     update_setting,
#     delete_setting
# )
# from app.db.schemas import SettingCreate, SettingUpdate, SettingInDB, UserCreate

# settings_router = r = APIRouter()

# @r.get(
#     "/settings",
#     response_model=t.List[SettingInDB],
#     response_model_exclude_none=True,
# )
# async def settings_list(
#     db: Session = Depends(get_db)
# ):
#     """
#     Get all settings as a single JSON object
#     """
#     settings = get_all_settings(db)
#     return settings

# @r.post(
# #  request: Request,
   
    
#     "/settings",
#     response_model=SettingInDB,
#     response_model_exclude_none=True, 
   
# )
# async def setting_create_or_update(
    
#     setting: SettingCreate,
#     db: Session = Depends(get_db)
# ):
#     """
#     Create a new setting or update an existing one
#     """
#     existing_setting = get_setting(db, setting.key)
#     if existing_setting:
#         updated_setting = update_setting(db, setting.key, SettingUpdate(value=setting.value))
#         return updated_setting
#     else:
#         new_setting = Setting(key=setting.key, value=setting.value)
#         db.add(new_setting)
#         db.commit()
#         db.refresh(new_setting)
#         return new_setting

# @r.delete(
#     "/settings/{key}",
#     response_model=SettingInDB,
#     response_model_exclude_none=True,
# )
# async def setting_delete(
#     key: str,
#     db: Session = Depends(get_db)
# ):
#     """
#     Delete a setting by key
#     """
#     setting = delete_setting(db, key)
#     if not setting:
#         raise HTTPException(status_code=404, detail="Setting not found")
#     return setting