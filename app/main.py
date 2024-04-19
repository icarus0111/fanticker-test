from fastapi import FastAPI
from fastapi.security import HTTPBasic
from passlib.context import CryptContext

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()


from app.apis.views import router as api_router
app.include_router(api_router, prefix="/api")
