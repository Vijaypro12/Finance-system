from fastapi import APIRouter, HTTPException
from sqlalchemy import Transaction
from sqlalchemy import Transaction
from sqlalchemy.orm import Session
from database import get_db
from models.TransactionModel import TransactionModel
from models.UserModel import UserModel
from schemas.schema import TransactionCreate, TransactionResponse, UserCreate, UserResponse
from fastapi import Depends
from dependencies import require_role
from typing import Optional
from datetime import datetime
from collections import defaultdict

router = APIRouter()


# Users routes
@router.post("/users", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(
        username=data.username,
        password=data.password,
        role=data.role

    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse.model_validate(db_user)


@router.get("/users", response_model=list[UserResponse])
def get_user(db : Session = Depends(get_db)):
    user = db.query(UserModel).all()
    return user


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id : int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user


@router.put("/users", response_model=UserResponse)
def update_user(user_id : int, data : UserCreate, db : Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    
    user.username = data.username
    user.password = data.password
    user.role = data.role
    
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.delete("/users/{user_id}")
def delete_user(user_id : int, db : Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


# Transactions routes
@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db), user = Depends(require_role(["admin"]))):
    db_trans = TransactionModel(
        amount=data.amount,
        type=data.type,
        category=data.category,
        date=data.date,
        notes=data.notes,
        user_id=data.user_id
    )
    db.add(db_trans)
    db.commit()
    db.refresh(db_trans)
    return TransactionResponse.model_validate(db_trans)


@router.get("/transactions")
def get_transactions(
    type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    user = Depends(require_role(["viewer", "analyst", "admin"]))
):
    query = db.query(TransactionModel)

    if type:
        query = query.filter(TransactionModel.type == type)

    if category:
        query = query.filter(TransactionModel.category == category)

    if start_date:
        query = query.filter(TransactionModel.date >= start_date)

    if end_date:
        query = query.filter(TransactionModel.date <= end_date)

    return query.all()

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db), user = Depends(require_role(["admin"]))):
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction with id {transaction_id} not found")
    return transaction

@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, data: TransactionCreate, db: Session = Depends(get_db), user = Depends(require_role(["admin"]))):
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction with id {transaction_id} not found")

    transaction.amount = data.amount
    transaction.type = data.type
    transaction.category = data.category
    transaction.date = data.date
    transaction.notes = data.notes
    transaction.user_id = data.user_id
    
    db.commit()
    db.refresh(transaction)
    return TransactionResponse.model_validate(transaction)

@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), user = Depends(require_role(["admin"]))):
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction with id {transaction_id} not found")
    
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}


@router.get("/summary")
def get_summary(user_id: int, db: Session = Depends(get_db), user = Depends(require_role(["viewer", "analyst", "admin"]))):
    transactions = db.query(TransactionModel).filter(TransactionModel.user_id == user_id).all()
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    balance = total_income - total_expense
    return {"total_income": total_income, "total_expense": total_expense, "balance": balance}


@router.get("/summary/category")
def category_summary(db: Session = Depends(get_db), user = Depends(require_role(["analyst", "admin"]))):
    transactions = db.query(TransactionModel).all()
    result = {}

    for t in transactions:
        if t.category not in result:
            result[t.category] = 0
        result[t.category] += t.amount

    return result

@router.get("/summary/monthly")
def monthly_summary(db: Session = Depends(get_db), user = Depends(require_role(["analyst", "admin"]))):
    transactions = db.query(TransactionModel).all()
    result = defaultdict(float)

    for t in transactions:
        key = t.date.strftime("%Y-%m")
        result[key] += t.amount

    return result

@router.get("/summary/recent")
def recent_transactions(user_id: int, limit: int = 5, db: Session = Depends(get_db), user = Depends(require_role(["viewer", "analyst", "admin"]))):
    transactions = (db.query(TransactionModel).filter(TransactionModel.user_id == user_id).order_by(TransactionModel.date.desc()).limit(limit).all())
    return transactions