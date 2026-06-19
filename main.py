from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import schemas
from models import City, Area,Client,User

from auth import verify_password
from fastapi.security import OAuth2PasswordRequestForm
from database import Base
from database import engine
from database import get_db

from jwt_token import create_access_token,admin_required,get_current_user,role_required

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = crud.get_user_by_email(
        db,
        form_data.username
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if not verify_password(
        form_data.password,
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

@app.post(
    "/users",
    response_model=schemas.UserResponse
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
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
@app.get(
    "/users",
    response_model=list[schemas.UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):

    return crud.get_users(db)

@app.get(
    "/users/{user_id}",
    response_model=schemas.UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = crud.get_user_by_id(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@app.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):

    return current_user

@app.get(
    "/cities",
    response_model=list[schemas.CityResponse]
)
def get_cities(
    db: Session = Depends(get_db)
):

    return crud.get_cities(db)

@app.get(
    "/cities/{city_id}/areas",
    response_model=list[schemas.AreaResponse]
)
def get_areas(
    city_id: int,
    db: Session = Depends(get_db)
):

    return crud.get_areas_by_city(
        db,
        city_id
    )

@app.post(
    "/clients",
    response_model=schemas.ClientResponse
)
def create_client(
    client: schemas.ClientCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing"]
    )
)
):

    return crud.create_client(
        db,
        client,
        current_user.id
    )

@app.get(
    "/clients",
    response_model=list[schemas.ClientResponse]
)
def get_clients(
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(["admin", "marketing", "sales"])
)
):

    return crud.get_clients(db)

@app.put(
    "/clients/{client_id}",
    response_model=schemas.ClientResponse
)
def update_client(
    client_id: int,
    data: schemas.ClientUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing"]
    )
)
):

    client = crud.update_client(
        db,
        client_id,
        data
    )

    if not client:

        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    return client

@app.delete(
    "/clients/{client_id}"
)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing"]
    )
)
):

    deleted = crud.delete_client(
        db,
        client_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    return {
        "message": "Client deleted successfully"
    }

@app.get(
    "/clients/search"
)
def search_clients(
    q: str,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(["admin", "marketing", "sales"])
)
):

    return crud.search_clients(
        db,
        q
    )

@app.get(
    "/clients/{client_id}",
    response_model=schemas.ClientResponse
)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(["admin", "marketing", "sales"])
)
):

    client = crud.get_client(
        db,
        client_id
    )

    if not client:

        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    return client

@app.post(
    "/existing-products",
    response_model=schemas.ExistingProductResponse
)
def create_existing_product(
    data: schemas.ExistingProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin"]
    )
)
):

    return crud.create_existing_product(
        db,
        data
    )

@app.get(
    "/existing-products",
    response_model=list[schemas.ExistingProductResponse]
)
def get_existing_products(
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing", "sales"]
    )
)
):

    return crud.get_existing_products(
        db
    )

@app.get(
    "/existing-products/search",
    response_model=list[schemas.ExistingProductResponse]
)
def search_existing_products(
    q: str,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing", "sales"]
    )
)
):

    return crud.search_existing_products(
        db,
        q
    )

@app.get(
    "/existing-products/{product_id}",
    response_model=schemas.ExistingProductResponse
)
def get_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing", "sales"]
    )
)
):

    product = crud.get_existing_product(
        db,
        product_id
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@app.put(
    "/existing-products/{product_id}",
    response_model=schemas.ExistingProductResponse
)
def update_existing_product(
    product_id: int,
    data: schemas.ExistingProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin"]
    )
)
):

    product = crud.update_existing_product(
        db,
        product_id,
        data
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@app.delete(
    "/existing-products/{product_id}"
)
def delete_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin"]
    )
)
):

    product = crud.delete_existing_product(
        db,
        product_id
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }

@app.post(
    "/call-logs",
    response_model=schemas.CallLogResponse
)
def create_call_log(
    data: schemas.CallLogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing"]
    )
)
):

    return crud.create_call_log(
        db,
        data
    )

@app.get(
    "/call-logs/search",
    response_model=list[schemas.CallLogResponse]
)
def search_call_logs(
    q: str,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing"]
    )
)
):

    return crud.search_call_logs(
        db,
        q
    )

@app.get(
    "/call-logs/{call_log_id}",
    response_model=schemas.CallLogResponse
)
def get_call_log(
    call_log_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing"]
    )
)
):

    call_log = crud.get_call_log(
        db,
        call_log_id
    )

    if not call_log:

        raise HTTPException(
            status_code=404,
            detail="Call Log not found"
        )

    return call_log

@app.get(
    "/call-logs",
    response_model=list[
        schemas.CallLogResponse
    ]
)
def get_call_logs(
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["admin", "marketing"]
        )
    )
):

    return crud.get_call_logs(db)

@app.put(
    "/call-logs/{call_log_id}",
    response_model=schemas.CallLogResponse
)
def update_call_log(
    call_log_id: int,
    data: schemas.CallLogUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing"]
    )
)
):

    call_log = crud.update_call_log(
        db,
        call_log_id,
        data
    )

    if not call_log:

        raise HTTPException(
            status_code=404,
            detail="Call Log not found"
        )

    return call_log

@app.get(
    "/clients/{client_id}/call-log-history",
    response_model=list[
        schemas.CallLogHistoryResponse
    ]
)
def get_call_log_history_by_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["admin", "marketing"]
        )
    )
):

    client = crud.get_client(
        db,
        client_id
    )

    if not client:

        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    return crud.get_call_log_history_by_client(
        db,
        client_id
    )

@app.delete(
    "/call-logs/{call_log_id}"
)
def delete_call_log(
    call_log_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing"]
    )
)
):

    call_log = crud.delete_call_log(
        db,
        call_log_id
    )

    if not call_log:

        raise HTTPException(
            status_code=404,
            detail="Call Log not found"
        )

    return {
        "message": "Call Log deleted successfully"
    }

@app.post(
    "/demos",
    response_model=schemas.DemoResponse
)
def create_demo(
    data: schemas.DemoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin","marketing", "sales"]
    )
)
):

    return crud.create_demo(
        db,
        data
    )

@app.get(
    "/demos",
    response_model=list[
        schemas.DemoResponse
    ]
)
def get_demos(
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing","sales"]
    )
)
):

    crud.check_expired_trials(db)

    return crud.get_demos(db)

@app.get(
    "/demos/search",
    response_model=list[
        schemas.DemoResponse
    ]
)
def search_demos(
    q: str,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin","marketing", "sales"]
    )
)
):

    return crud.search_demos(
        db,
        q
    )

@app.get(
    "/demos/{demo_id}",
    response_model=schemas.DemoResponse
)
def get_demo(
    demo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin","marketing", "sales"]
    )
)
):

    demo = crud.get_demo(
        db,
        demo_id
    )

    if not demo:

        raise HTTPException(
            status_code=404,
            detail="Demo not found"
        )

    return demo

@app.put(
    "/demos/{demo_id}",
    response_model=schemas.DemoResponse
)
def update_demo(
    demo_id: int,
    data: schemas.DemoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing","sales"]
    )
)
):

    demo = crud.update_demo(
        db,
        demo_id,
        data
    )

    if not demo:

        raise HTTPException(
            status_code=404,
            detail="Demo not found"
        )

    return demo

@app.delete(
    "/demos/{demo_id}"
)
def delete_demo(
    demo_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing","sales"]
    )
)
):

    demo = crud.delete_demo(
        db,
        demo_id
    )

    if not demo:

        raise HTTPException(
            status_code=404,
            detail="Demo not found"
        )

    return {
        "message": "Demo deleted successfully"
    }

@app.post(
    "/deals",
    response_model=schemas.DealResponse
)
def create_deal(
    data: schemas.DealCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "sales"]
    )
)
):

    return crud.create_deal(
        db,
        data
    )

@app.get(
    "/deals",
    response_model=list[schemas.DealResponse]
)
def get_deals(
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "sales"]
    )
)
):

    return crud.get_deals(db)

@app.get(
    "/deals/search",
    response_model=list[schemas.DealResponse]
)
def search_deals(
    q: str,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "sales"]
    )
)
):

    return crud.search_deals(
        db,
        q
    )

@app.get(
    "/deals/{deal_id}",
    response_model=schemas.DealResponse
)
def get_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "sales"]
    )
)
):

    deal = crud.get_deal(
        db,
        deal_id
    )

    if not deal:

        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )

    return deal

@app.put(
    "/deals/{deal_id}",
    response_model=schemas.DealResponse
)
def update_deal(
    deal_id: int,
    data: schemas.DealUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "sales"]
    )
)
):

    deal = crud.update_deal(
        db,
        deal_id,
        data
    )

    if not deal:

        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )

    return deal

@app.delete("/deals/{deal_id}")
def delete_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "sales"]
    )
)
):

    success = crud.delete_deal(
        db,
        deal_id
    )

    if not success:

        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )

    return {
        "message": "Deal deleted successfully"
    }

@app.get(
    "/reminders",
    response_model=list[
        schemas.ReminderResponse
    ]
)
def get_reminders(
    db: Session = Depends(get_db),
    current_user=Depends(
    role_required(
        ["admin", "marketing", "sales"]
    )
)
):

    return crud.get_reminders(db)