# crud.users.py
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.utils import get_password_hash
from app.schemas.users import UserCreate
from app.db.models import User
from uuid import uuid4
from app.db.database import get_db


def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    db_user = User(
        id=uuid4(), email=user.email, hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
