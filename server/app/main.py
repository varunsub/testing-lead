from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import leads, auth
from app.db.database import engine, database
from app.db import models
from app.crud.users import create_user, get_user_by_email
import os
from app.db.database import SessionLocal
from app.schemas.users import UserCreate

models.Base.metadata.create_all(bind=engine)

# ENV
TO_EMAIL = os.getenv("TO_EMAIL")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    db = SessionLocal()
    res = get_user_by_email(db=db, email=TO_EMAIL)
    if not res:
        attorney = UserCreate(email=TO_EMAIL, password="password")
        create_user(user=attorney, db=db)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(leads.router, prefix="/leads", tags=["leads"])
