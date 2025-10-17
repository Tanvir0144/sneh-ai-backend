from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class UserInDBBase(UserBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True # Pydantic v2 uses this instead of orm_mode

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str