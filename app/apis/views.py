from fastapi.security import HTTPBasicCredentials

from app.main import app, security
from fastapi import HTTPException, Depends, status, Security, APIRouter

from app.utile.auth import authenticate_user
from app.utile.counter import get_counter, increment_counter_value
from core.db import get_db

router = APIRouter()


@router.get("/counter", response_model=dict)
def read_counter(db=Depends(get_db), credentials: HTTPBasicCredentials = Security(security)):
    user = authenticate_user(credentials)
    if "counter-reader" not in user["roles"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to access this endpoint")
    return {"counter": get_counter(db)}


@router.put("/counter", response_model=dict)
def increment_counter(db=Depends(get_db), credentials: HTTPBasicCredentials = Security(security)):
    user = authenticate_user(credentials)
    if "counter-incrementer" not in user["roles"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to access this endpoint")
    increment_counter_value(db)
    return {"message": "Counter incremented successfully"}
