from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import UUID


class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class LeadCreate(LeadBase):
    resume: str


class Lead(LeadBase):
    id: UUID
    resume: str
    state: str

    class Config:
        orm_mode: True


class LeadStateUpdate(BaseModel):
    state: str


class PaginatedLead(BaseModel):
    total: int
    leads: List[Lead]
