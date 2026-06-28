from datetime import date

from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):

    full_name: str

    dob: date

    mobile_no: str

    email: EmailStr

    aadhar_no: str

    pan_no: str

    address: str
