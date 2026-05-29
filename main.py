from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

import crud
import schemas

from auth import verify_password

from database import Base
from database import engine
from database import get_db

from jwt_token import create_access_token

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():

    return {
        "message": "CRM Backend Running Successfully"
    }


# SIGNUP API
@app.post(
    "/signup",
    response_model=schemas.UserResponse
)
def signup(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = crud.get_user_by_email(
        db,
        user.email
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return crud.create_user(
        db,
        user
    )


# LOGIN API
@app.post(
    "/login",
    response_model=schemas.Token
)
def login(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):

    db_user = crud.get_user_by_email(
        db,
        user.email
    )

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }