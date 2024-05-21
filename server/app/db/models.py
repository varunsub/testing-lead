import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class Lead(Base):
    __tablename__ = "leads"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    first_name = sa.Column(sa.String(255), index=True)  # Added length constraint
    last_name = sa.Column(sa.String(255), index=True)  # Added length constraint
    email = sa.Column(
        sa.String(255), index=True, unique=True
    )  # Added unique constraint
    resume = sa.Column(sa.String(255))  # Added length constraint
    state = sa.Column(
        sa.String(50), index=True, default="PENDING"
    )  # Added length constraint


class User(Base):
    __tablename__ = "users"
    id = sa.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email = sa.Column(
        sa.String(255), unique=True, index=True
    )  # Added length constraint
    hashed_password = sa.Column(sa.String(255))  # Added length constraint
