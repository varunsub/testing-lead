from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, Form
from sqlalchemy import func
from sqlalchemy.orm import Session
from uuid import UUID
from app.crud import leads as crud_leads
from app.schemas import users as schema_users, leads as schema_leads
from app.db.database import get_db
from app.core.security import get_current_user
import uuid
from app.core.email import send_email
import os

from app.db.models import Lead
from app.core.gcloud import upload_to_gcs

router = APIRouter()
TO_EMAIL = os.getenv("TO_EMAIL")


@router.post("/", response_model=schema_leads.Lead)
async def create_lead(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    resume: UploadFile = Form(...),
    db: Session = Depends(get_db),
):
    resume_filename = f"{uuid.uuid4()}_{resume.filename}"
    resume_path = f"resumes/{resume_filename}"
    with open(resume_path, "wb") as buffer:
        buffer.write(await resume.read())

    gcs_url = upload_to_gcs(
        os.environ.get("BUCKET_NAME"), resume_path, f"resumes/{resume_filename}"
    )
    if not gcs_url:
        raise HTTPException(status_code=500, detail="Failed to upload resume")

    lead = await crud_leads.create_lead(db, first_name, last_name, email, gcs_url)
    subject = "Thank you for your submission"
    prospect_email_content = f"""
    <p>Dear {first_name} {last_name},</p>
    <p>Thank you for submitting your resume. We will review it and get back to you soon.</p>
    """
    send_email(subject, lead.email, prospect_email_content)

    attorney_email_content = f"""
    <p>A new lead has been submitted:</p>
    <ul>
        <li>Name: {first_name} {last_name}</li>
        <li>Email: {email}</li>
    </ul>
    <p>Please review the resume attached.</p>
    """
    send_email("New Lead Submitted", TO_EMAIL, attorney_email_content, gcs_url)

    return lead


@router.get("/", response_model=schema_leads.PaginatedLead)
def read_leads(
    request: Request,
    skip: int = 0,
    limit: int = 1,
    db: Session = Depends(get_db),
    current_user: schema_users.User = Depends(get_current_user),
):
    leads = crud_leads.get_leads(db, skip=skip, limit=limit)
    total_leads = db.query(func.count(Lead.id)).scalar()
    for lead in leads:
        if lead.resume is None:
            lead.resume = ""
    return {"total": total_leads, "leads": leads}


@router.patch("/{lead_id}", response_model=schema_leads.Lead)
async def update_lead_state(
    lead_id: UUID,
    lead_state: schema_leads.LeadStateUpdate,
    db: Session = Depends(get_db),
    current_user: schema_users.User = Depends(get_current_user),
):
    lead = crud_leads.update_lead_state(db, lead_id, lead_state.state)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead
