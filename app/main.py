from fastapi import FastAPI, HTTPException, Depends, status, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
from pydantic import BaseModel
from passlib.context import CryptContext


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Counter(Base):
  __tablename__ = "counter"
  id = Column(Integer, primary_key=True, index=True)
  value = Column(Integer, default=0)


Base.metadata.create_all(bind=engine)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


users = {
  "user1": {
    "username": "user1",
    "password": pwd_context.hash("password1"),
    "disabled": False,
    "roles": ["counter-reader"]
  },
  "user2": {
    "username": "user2",
    "password": pwd_context.hash("password2"),
    "disabled": False,
    "roles": ["counter-incrementer"]
  }
}


app = FastAPI()


@app.get("/api/counter", response_model=dict)
def read_counter(db=Depends(get_db), credentials: HTTPBasicCredentials = Security(security)):
  user = authenticate_user(credentials)
  if "counter-reader" not in user["roles"]:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this endpoint")
  return {"counter": get_counter(db)}


@app.put("/api/counter", response_model=dict)
def increment_counter(db=Depends(get_db), credentials: HTTPBasicCredentials = Security(security)):
  user = authenticate_user(credentials)
  if "counter-incrementer" not in user["roles"]:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this endpoint")
  increment_counter_value(db)
  return {"message": "Counter incremented successfully"}


def get_counter(db):
  counter = db.query(Counter).first()
  if counter:
    return counter.value
  else:
    return 0


def increment_counter_value(db):
  counter = db.query(Counter).first()
  if counter:
    counter.value += 1
  else:
    new_counter = Counter(value=1)
    db.add(new_counter)
  db.commit()


def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(credentials: HTTPBasicCredentials):
  user = users.get(credentials.username)
  if not user or not verify_password(credentials.password, user["password"]):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
  return user
