from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    first_name: str
    last_name: str
    mobile_no: str

    class Config:
        from_attributes = True
