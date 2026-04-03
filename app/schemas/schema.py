from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy import Column
from enum import Enum

# Enums for transaction type and user role
class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

class UserType(str, Enum):
    viewer = "viewer"
    analyst = "analyst" 
    admin = "admin"     

# Schemas for users
class UserCreate(BaseModel):
    username : str
    password : str
    role : UserType

class UserResponse(BaseModel):
    id : int
    username : str
    role : UserType

    class Config:
        from_attributes = True    

# Schemas for transactions
class TransactionCreate(BaseModel):
     amount : float = Field(gt=0)
     type: TransactionType
     category : str
     date : datetime
     notes : str
     user_id : int

class TransactionResponse(BaseModel):
      id : int
      amount : float
      type : str
      category : str
      date : datetime
      notes : str
      user_id : int
    
      class Config:
        from_attributes = True