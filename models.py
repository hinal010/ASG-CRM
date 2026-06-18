from sqlalchemy import Column, Integer, String, ForeignKey, Date,Time,Float
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import UniqueConstraint
from datetime import datetime
from zoneinfo import ZoneInfo

def india_date():
    return datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).date()


def india_time():
    return datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).time()


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        nullable=False,
        default="user"
    )
    clients = relationship(
    "Client",
    back_populates="creator"
    )

    demos = relationship(
    "Demo",
    back_populates="assigned_employee"
)

class City(Base):

    __tablename__ = "cities"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    areas = relationship(
        "Area",
        back_populates="city"
    )

class Area(Base):

    __tablename__ = "areas"

    __table_args__ = (
        UniqueConstraint(
            "name",
            "city_id",
            name="uq_area_city"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    city_id = Column(
        Integer,
        ForeignKey("cities.id")
    )

    city = relationship(
        "City",
        back_populates="areas"
    )

class Client(Base):

    __tablename__ = "clients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    pharmacy_name = Column(
        String,
        nullable=False
    )

    contact_person = Column(
        String
    )

    mobile_no = Column(
        String(10),
        nullable=False
    )

    email = Column(
        String
    )

    lead_source = Column(
        String
    )

    address = Column(
        String
    )

    city_id = Column(
        Integer,
        ForeignKey("cities.id"),
        nullable=False
    )

    area_id = Column(
        Integer,
        ForeignKey("areas.id"),
        nullable=False
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    creator = relationship(
        "User",
        back_populates="clients"
    )

    city = relationship(
        "City"
    )

    area = relationship(
        "Area"
    )
    
    call_logs = relationship(
    "CallLog",
    back_populates="client"
)
    demos = relationship(
    "Demo",
    back_populates="client"
)
    deals = relationship(
    "Deal",
    back_populates="client"
)


class ExistingProduct(Base):

    __tablename__ = "existing_products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_name = Column(
        String,
        unique=True,
        nullable=False
    )

class CallLog(Base):

    __tablename__ = "call_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    client_id = Column(
        Integer,
        ForeignKey("clients.id")
    )

    existing_product_id = Column(
        Integer,
        ForeignKey("existing_products.id"),
        nullable=True
    )

    lead_status = Column(
        String,
        nullable=False
    )

    remarks = Column(String)

    follow_up_date = Column(Date)

    # created_date = Column(
    #     Date,
    #     default=lambda: datetime.now().date()
    # )

    # created_time = Column(
    #     Time,
    #     default=lambda: datetime.now().time()
    # )
    created_date = Column(
    Date,
    default=india_date
    )

    created_time = Column(
        Time,
        default=india_time
    )

    existing_product = relationship(
        "ExistingProduct"
    )

    client = relationship(
        "Client",
        back_populates="call_logs"
    )


class Demo(Base):

    __tablename__ = "demos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=False
    )

    assigned_employee_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    demo_date = Column(
        Date,
        nullable=False
    )

    demo_time = Column(
        Time,
        nullable=False
    )

    demo_feedback = Column(
        String
    )

    meeting_notes = Column(
        String
    )

    demo_status = Column(
        String,
        nullable=False
    )

    demo_location = Column(
        String
    )

    demo_installed = Column(
        String,
        default="No"
    )

    installation_date = Column(
        Date
    )

    trial_days = Column(
        Integer,
        default=10
    )

    trial_expiry_date = Column(
        Date
    )

    trial_status = Column(
        String,
        default="active"
    )

    client = relationship(
        "Client",
        back_populates="demos"
    )

    assigned_employee = relationship(
    "User",
    back_populates="demos"
)
    

class Deal(Base):

    __tablename__ = "deals"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    client_id = Column(
        Integer,
        ForeignKey("clients.id")
    )

    deal_owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    deal_name = Column(String)

    software_type = Column(String)

    amount = Column(Float)

    number_of_devices = Column(Integer)

    start_date = Column(Date)

    end_date = Column(Date)

    renewal_reminder_date = Column(Date)

    renewal_status = Column(
        String,
        default="active"
    )

    notes = Column(String)

    # created_date = Column(
    #     Date,
    #     default=lambda: datetime.now().date()
    # )

    # created_time = Column(
    #     Time,
    #     default=lambda: datetime.now().time()
    # )
    created_date = Column(
    Date,
    default=india_date
    )

    created_time = Column(
        Time,
        default=india_time
    )

    client = relationship(
        "Client",
        back_populates="deals"
    )

    deal_owner = relationship(
        "User"
    )