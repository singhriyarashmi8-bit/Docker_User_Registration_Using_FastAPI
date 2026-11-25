from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints
from typing import Annotated

Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=120)]
Phone = Annotated[str, StringConstraints(strip_whitespace=True, min_length=7, max_length=30)]

class UserCreate(BaseModel):
    full_name: Name
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    phone_number: Phone

class UserUpdate(BaseModel):
    full_name: Name | None = None
    email: EmailStr | None = None
    phone_number: Phone | None = None

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: EmailStr
    phone_number: str
    created_at: datetime
    updated_at: datetime
