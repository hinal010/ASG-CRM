from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import UniqueConstraint


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