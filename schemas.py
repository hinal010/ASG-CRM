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

class ClientCreate(BaseModel):

    pharmacy_name: str
    contact_person: str | None = None
    mobile_no: str

    email: EmailStr | None = None
    lead_source: str | None = None
    address: str | None = None

    city_id: int
    area_id: int

class ClientUpdate(BaseModel):

    pharmacy_name: str
    contact_person: str | None = None
    mobile_no: str

    email: EmailStr | None = None
    lead_source: str | None = None
    address: str | None = None

    city_id: int
    area_id: int

class ClientResponse(BaseModel):

    id: int

    pharmacy_name: str
    contact_person: str | None

    mobile_no: str

    email: EmailStr | None
    lead_source: str | None
    address: str | None

    city_id: int
    area_id: int

    created_by: int

    class Config:
        from_attributes = True