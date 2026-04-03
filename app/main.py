from fastapi import FastAPI
from database import Base, engine
from routes import routes
from models.UserModel import UserModel
from models.TransactionModel import TransactionModel

app = FastAPI()

app.include_router(routes.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def hello():
    return {"message": "Hello World"}