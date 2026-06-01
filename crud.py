from sqlalchemy.orm import Session

from models import User, City, Area

from schemas import UserCreate

from auth import hash_password


def get_user_by_email(
    db: Session,
    email: str
):

    return db.query(User).filter(
        User.email == email
    ).first()


def create_user(
    db: Session,
    user: UserCreate
):

    hashed_password = hash_password(
        user.password
    )

    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_cities(db):

    return db.query(
        City
    ).order_by(
        City.name
    ).all()


def get_areas_by_city(
    db,
    city_id: int
):

    return db.query(
        Area
    ).filter(
        Area.city_id == city_id
    ).order_by(
        Area.name
    ).all()