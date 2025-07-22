from pydantic import BaseModel, EmailStr, Field
from typing import Literal ,Optional

class UserCreate(BaseModel):
    role: Literal["student", "teacher", "admin", "organization"]
    full_name: str
    university_name: str
    mobile_number: str
    email: EmailStr
    password: str
    confirm_password: str

class UserLogin(BaseModel):
    identifier: str  # email or mobile number
    password: str
    remember: Optional[bool] = False  # ✅ optional field with default False

class UserOut(BaseModel):
    id: str
    full_name: str
    role: str
    email: EmailStr
