from sqlalchemy.orm import Session

from models import User, City, Area,Client,ExistingProduct,CallLog

from schemas import UserCreate

from auth import hash_password
from fastapi import HTTPException


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

def create_client(
    db,
    client,
    user_id
):

    db_client = Client(
        pharmacy_name=client.pharmacy_name,
        contact_person=client.contact_person,
        mobile_no=client.mobile_no,
        email=client.email,
        lead_source=client.lead_source,
        address=client.address,
        city_id=client.city_id,
        area_id=client.area_id,
        created_by=user_id
    )

    db.add(db_client)

    db.commit()

    db.refresh(db_client)

    return db_client

def get_clients(
    db,
    skip=0,
    limit=100
):

    return db.query(
        Client
    ).offset(
        skip
    ).limit(
        limit
    ).all()

def get_client(
    db,
    client_id
):

    return db.query(
        Client
    ).filter(
        Client.id == client_id
    ).first()

def update_client(
    db,
    client_id,
    data
):

    client = db.query(
        Client
    ).filter(
        Client.id == client_id
    ).first()

    if not client:
        return None

    update_data = data.model_dump(
    exclude_unset=True
        )

    for key, value in update_data.items():

        setattr(
            client,
            key,
            value
        )

    db.commit()

    db.refresh(client)

    return client

def delete_client(
    db,
    client_id
):

    client = db.query(
        Client
    ).filter(
        Client.id == client_id
    ).first()

    if not client:
        return False

    db.delete(client)

    db.commit()

    return True

def search_clients(
    db,
    query
):

    return db.query(
        Client
    ).filter(
        Client.pharmacy_name.ilike(
            f"%{query}%"
        )
    ).all()

def create_existing_product(
    db,
    data
):

    product = ExistingProduct(
        **data.model_dump()
    )

    db.add(product)

    db.commit()

    db.refresh(product)

    return product

def get_existing_products(
    db
):

    return db.query(
        ExistingProduct
    ).all()

def get_existing_product(
    db,
    product_id
):

    return db.query(
        ExistingProduct
    ).filter(
        ExistingProduct.id == product_id
    ).first()

def update_existing_product(
    db,
    product_id,
    data
):

    product = db.query(
        ExistingProduct
    ).filter(
        ExistingProduct.id == product_id
    ).first()

    if not product:
        return None

    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(
            product,
            key,
            value
        )

    db.commit()

    db.refresh(product)

    return product

def delete_existing_product(
    db,
    product_id
):

    product = db.query(
        ExistingProduct
    ).filter(
        ExistingProduct.id == product_id
    ).first()

    if not product:
        return None

    db.delete(product)

    db.commit()

    return True

def search_existing_products(
    db,
    q
):

    return db.query(
        ExistingProduct
    ).filter(
        ExistingProduct.product_name.ilike(
            f"%{q}%"
        )
    ).all()

def create_call_log(
    db,
    data
):

    client = db.query(
        Client
    ).filter(
        Client.id == data.client_id
    ).first()

    if not client:

        raise HTTPException(
            status_code=404,
            detail="Client not found"
        )

    if data.existing_product_id:

        product = db.query(
            ExistingProduct
        ).filter(
            ExistingProduct.id == data.existing_product_id
        ).first()

        if not product:

            raise HTTPException(
                status_code=404,
                detail="Existing Product not found"
            )

    call_log = CallLog(
        **data.model_dump()
    )

    db.add(call_log)

    db.commit()

    db.refresh(call_log)

    return call_log
def get_call_logs(
    db
):

    return db.query(
        CallLog
    ).all()

def get_call_log(
    db,
    call_log_id
):

    return db.query(
        CallLog
    ).filter(
        CallLog.id == call_log_id
    ).first()

def update_call_log(
    db,
    call_log_id,
    data
):

    call_log = db.query(
        CallLog
    ).filter(
        CallLog.id == call_log_id
    ).first()

    if not call_log:
        return None
    
    if "client_id" in update_data:

        client = db.query(
            Client
        ).filter(
            Client.id == update_data["client_id"]
        ).first()

        if not client:

            raise HTTPException(
                status_code=404,
                detail="Client not found"
            )
        
    if ("existing_product_id" in update_data 
        and update_data["existing_product_id"] is not None
):

        product = db.query(
            ExistingProduct
        ).filter(
            ExistingProduct.id == update_data["existing_product_id"]
        ).first()

        if not product:

            raise HTTPException(
                status_code=404,
                detail="Existing Product not found"
            )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(
            call_log,
            key,
            value
        )

    db.commit()

    db.refresh(call_log)

    return call_log

def delete_call_log(
    db,
    call_log_id
):

    call_log = db.query(
        CallLog
    ).filter(
        CallLog.id == call_log_id
    ).first()

    if not call_log:
        return None

    db.delete(call_log)

    db.commit()

    return True

# Search by remarks or lead status:
def search_call_logs(
    db,
    q
):

    return db.query(
        CallLog
    ).filter(
        (CallLog.lead_status.ilike(f"%{q}%")) |
        (CallLog.remarks.ilike(f"%{q}%"))
    ).all()