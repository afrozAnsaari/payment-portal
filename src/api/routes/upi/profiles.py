from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from src.databases.crud import create_upi_profile

from src.databases.database import get_db

from src.schemas.upi_profile import UPIProfileCreate

router = APIRouter(tags=["upi_profiles"])


@router.post("/upi_profile")
def create_profile(profile: UPIProfileCreate, db: Session = Depends(get_db)):

    return create_upi_profile(db, profile_data=profile)
