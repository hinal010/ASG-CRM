from pydantic import BaseModel
from pydantic import EmailStr


class UserCreate(BaseModel):

    name: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):

    email: EmailStr
    password: str


class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    role: str

    class Config:

        from_attributes = True


class Token(BaseModel):

    access_token: str
    token_type: str

class CityResponse(BaseModel):

    id: int
    name: str

    class Config:
        from_attributes = True

class AreaResponse(BaseModel):

    id: int
    name: str
    city_id: int

    class Config:
        from_attributes = True