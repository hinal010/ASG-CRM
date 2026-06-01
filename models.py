from sqlalchemy import Column, Integer, String, ForeignKey, Date,Time
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import UniqueConstraint
from datetime import datetime


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

    created_date = Column(
        Date,
        default=lambda: datetime.now().date()
    )

    created_time = Column(
        Time,
        default=lambda: datetime.now().time()
    )

    existing_product = relationship(
        "ExistingProduct"
    )

    client = relationship(
        "Client",
        back_populates="call_logs"
    )
