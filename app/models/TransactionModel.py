from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey

class TransactionModel(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key = True, index = True)
    amount = Column(Float)
    type = Column(String)
    category = Column(String)
    date = Column(DateTime)
    notes = Column(String)
    user_id = Column(ForeignKey("users.id"))