from pydantic import BaseModel
from pydantic import EmailStr,Field
from datetime import date ,time


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

class ExistingProductCreate(BaseModel):

    product_name: str

class ExistingProductUpdate(BaseModel):

    product_name: str | None = None

class ExistingProductResponse(BaseModel):

    id: int

    product_name: str

    class Config:

        from_attributes = True

class CallLogCreate(BaseModel):

    client_id: int

    existing_product_id: int | None = None

    lead_status: str

    remarks: str | None = None

    follow_up_date: date | None = None

class CallLogUpdate(BaseModel):

    client_id: int | None = None

    existing_product_id: int | None = None

    lead_status: str | None = None

    remarks: str | None = None

    follow_up_date: date | None = None

class CallLogResponse(BaseModel):

    id: int

    client_id: int

    existing_product_id: int | None

    lead_status: str

    remarks: str | None

    follow_up_date: date | None

    created_date: date

    created_time: time

    class Config:

        from_attributes = True

class DemoCreate(BaseModel):

    client_id: int

    assigned_employee_id: int

    demo_date: date

    demo_time: time

    demo_feedback: str | None = None

    meeting_notes: str | None = None

    demo_status: str

    demo_location: str | None = None

    demo_installed: str = "No"

    installation_date: date | None = None

    trial_days: int = 10


class DemoUpdate(BaseModel):

    client_id: int | None = None

    assigned_employee_id: int | None = None

    demo_date: date | None = None

    demo_time: time | None = None

    demo_feedback: str | None = None

    meeting_notes: str | None = None

    demo_status: str | None = None

    demo_location: str | None = None

    demo_installed: str | None = None

    installation_date: date | None = None

    trial_days: int | None = None


class DemoResponse(BaseModel):

    id: int

    client_id: int

    assigned_employee_id: int

    demo_date: date

    demo_time: time

    demo_feedback: str | None

    meeting_notes: str | None

    demo_status: str

    demo_location: str | None

    demo_installed: str

    installation_date: date | None

    trial_days: int

    trial_expiry_date: date | None

    trial_status: str

    # created_date: date

    # created_time: time

    class Config:

        from_attributes = True