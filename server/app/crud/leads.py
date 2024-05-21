from sqlalchemy.orm import Session
import uuid
from app.db.models import Lead


async def create_lead(
    db: Session, first_name: str, last_name: str, email: str, resume: str
):
    lead_id = uuid.uuid4()
    new_lead = Lead(
        id=lead_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        resume=resume,
        state="PENDING",
    )
    try:
        db.add(new_lead)
        db.commit()
        new_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    except Exception as e:
        db.rollback()
        raise e
    return new_lead


def get_leads(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Lead).offset(skip).limit(limit).all()


def update_lead_state(db: Session, lead_id: uuid.UUID, state: str):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if lead:
        lead.state = state
        try:
            db.commit()
            db.refresh(lead)
        except Exception as e:
            db.rollback()
            raise e
    return lead
