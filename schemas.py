from pydantic import BaseModel
from pydantic import EmailStr,Field


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
    mobile_no: str = Field(
    min_length=10,
    max_length=10
)

    email: EmailStr | None = None
    lead_source: str | None = None
    address: str | None = None

    city_id: int
    area_id: int

class ClientUpdate(BaseModel):

    pharmacy_name: str | None = None
    contact_person: str | None = None
    mobile_no: str | None = Field(
        default=None,
        min_length=10,
        max_length=10
    )

    email: EmailStr | None = None
    lead_source: str | None = None
    address: str | None = None

    city_id: int | None = None
    area_id: int | None = None

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

    # city_name: str
    # area_name: str


    created_by: int

    class Config:
        from_attributes = True