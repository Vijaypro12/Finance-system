from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.UserModel import UserModel

# Get the current user
def get_current_user(user_id : int, db:Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Role Checking
def require_role(allowed_list:list):
    def role_checker(user = Depends(get_current_user)):
        if user.role not in allowed_list:
            raise HTTPException(status_code=403, detail="Access Denied")
        return user

    return role_checker