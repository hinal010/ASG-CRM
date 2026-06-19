from http import client

from sqlalchemy.orm import Session

from models import User, City, Area,Client,ExistingProduct,CallLog,Demo,Deal ,CallLogHistory

from schemas import UserCreate

from auth import hash_password
from fastapi import HTTPException
from datetime import timedelta
from datetime import date
from urllib.parse import quote
from sqlalchemy import or_


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

def get_call_logs(
    db
):

    return db.query(
        CallLog
    ).order_by(
        CallLog.created_date.desc(),
        CallLog.created_time.desc()
    ).all()

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

    history = CallLogHistory(
        client_id=call_log.client_id,
        call_log_id=call_log.id,
        existing_product_id=call_log.existing_product_id,
        lead_status=call_log.lead_status,
        remarks=call_log.remarks,
        follow_up_date=call_log.follow_up_date
    )

    db.add(history)

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

def get_call_log_history_by_client(
    db,
    client_id
):

    return db.query(
        CallLogHistory
    ).filter(
        CallLogHistory.client_id == client_id
    ).order_by(
        CallLogHistory.updated_date,
        CallLogHistory.updated_time
    ).all()

def create_demo(
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
    map_url = None

    if client.address:

        map_url = (
            "https://www.google.com/maps/search/?api=1&query="
            + quote(client.address)
        )

    employee = db.query(
        User
    ).filter(
        User.id == data.assigned_employee_id
    ).first()

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    trial_expiry_date = None

    if data.installation_date:

        trial_expiry_date = (
            data.installation_date
            + timedelta(days=data.trial_days)
        )

    demo_data = data.model_dump()

    demo_data["demo_location"] = map_url

    demo = Demo(
        **demo_data,
        trial_expiry_date=trial_expiry_date,
        trial_status="active"
    )
        

    db.add(demo)

    db.commit()

    db.refresh(demo)

    return demo

def get_demos(db):

    return db.query(
        Demo
    ).all()

def get_demo(
    db,
    demo_id
):

    return db.query(
        Demo
    ).filter(
        Demo.id == demo_id
    ).first()

def update_demo(
    db,
    demo_id,
    data
):

    demo = db.query(
        Demo
    ).filter(
        Demo.id == demo_id
    ).first()

    if not demo:
        return None

    update_data = data.model_dump(
        exclude_unset=True
    )

    if (
        "client_id" in update_data
    ):

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
        
        if client.address:

            demo.demo_location = (
                "https://www.google.com/maps/search/?api=1&query="
                + quote(client.address)
        )

    if (
        "assigned_employee_id" in update_data
    ):

        employee = db.query(
            User
        ).filter(
            User.id == update_data["assigned_employee_id"]
        ).first()

        if not employee:

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

    for key, value in update_data.items():

        setattr(
            demo,
            key,
            value
        )

    if demo.installation_date:

        demo.trial_expiry_date = (
            demo.installation_date
            + timedelta(days=demo.trial_days)
        )

    db.commit()

    db.refresh(demo)

    return demo

def delete_demo(
    db,
    demo_id
):

    demo = db.query(
        Demo
    ).filter(
        Demo.id == demo_id
    ).first()

    if not demo:
        return None

    db.delete(demo)

    db.commit()

    return demo

def search_demos(
    db,
    q
):

    return db.query(
        Demo
    ).join(
        Client
    ).filter(
        Client.pharmacy_name.ilike(
            f"%{q}%"
        )
    ).all()


def check_expired_trials(db):

    demos = db.query(
        Demo
    ).filter(
        Demo.trial_status == "active"
    ).all()

    today = date.today()

    for demo in demos:

        if (
            demo.trial_expiry_date
            and demo.trial_expiry_date < today
        ):

            demo.trial_status = "expired"

    db.commit()

def create_deal(
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

    user = db.query(
        User
    ).filter(
        User.id == data.deal_owner_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    deal = Deal(
        **data.model_dump(),
        renewal_reminder_date=data.end_date,
        renewal_status="active"
    )

    db.add(deal)

    db.commit()

    db.refresh(deal)

    return deal

def get_deals(db):

    return db.query(
        Deal
    ).all()

def get_deal(
    db,
    deal_id
):

    return db.query(
        Deal
    ).filter(
        Deal.id == deal_id
    ).first()

def update_deal(
    db,
    deal_id,
    data
):

    deal = db.query(
        Deal
    ).filter(
        Deal.id == deal_id
    ).first()

    if not deal:

        return None

    update_data = data.model_dump(
        exclude_unset=True
    )

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

    if "deal_owner_id" in update_data:

        user = db.query(
            User
        ).filter(
            User.id == update_data["deal_owner_id"]
        ).first()

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

    if "end_date" in update_data:

        deal.renewal_reminder_date = update_data["end_date"]

    for key, value in update_data.items():

        setattr(
            deal,
            key,
            value
        )

    db.commit()

    db.refresh(deal)

    return deal

def delete_deal(
    db,
    deal_id
):

    deal = db.query(
        Deal
    ).filter(
        Deal.id == deal_id
    ).first()

    if not deal:

        return False

    db.delete(deal)

    db.commit()

    return True

def search_deals(
    db,
    q
):

    return db.query(
        Deal
    ).join(
        Client
    ).filter(
        or_(
            Deal.deal_name.ilike(f"%{q}%"),
            Deal.software_type.ilike(f"%{q}%"),
            Client.pharmacy_name.ilike(f"%{q}%")
        )
    ).all()

def get_reminders(
    db,
    current_user
):

    reminders = []

    today = date.today()

    next_7_days = today + timedelta(days=7)

    next_15_days = today + timedelta(days=15)

    next_30_days = today + timedelta(days=30)

    expired_deals = db.query(
        Deal
    ).filter(
        Deal.renewal_status == "active",
        Deal.renewal_reminder_date != None,
        Deal.renewal_reminder_date < today
    ).all()

    for deal in expired_deals:

        deal.renewal_status = "inactive"

    db.commit()

    if current_user.role in [
        "admin",
        "marketing"
    ]:

        call_logs = db.query(
            CallLog
        ).join(
            Client
        ).filter(
            CallLog.follow_up_date != None,
            CallLog.follow_up_date <= next_7_days,
            CallLog.lead_status.in_([
                "interested",
                "call_later",
                "no_response"
            ])
        ).all()

        for log in call_logs:

            if log.follow_up_date < today:

                status = "Overdue"

            elif log.follow_up_date == today:

                status = "Today"

            else:

                status = "Upcoming"

            reminders.append({
                "reminder_type": "Follow Up",
                "client_id": log.client_id,
                "client_name": log.client.pharmacy_name,
                "reminder_date": log.follow_up_date,
                "status": status
            })

    if current_user.role in [
        "admin",
        "sales"
    ]:

        scheduled_demos = db.query(
            Demo
        ).join(
            Client
        ).filter(
            Demo.demo_status == "scheduled",
            Demo.demo_date != None,
            Demo.demo_date >= today,
            Demo.demo_date <= next_7_days
        ).all()

        for demo in scheduled_demos:

            reminders.append({
                "reminder_type": "Demo Scheduled",
                "client_id": demo.client_id,
                "client_name": demo.client.pharmacy_name,
                "reminder_date": demo.demo_date,
                "status": "Scheduled"
            })

        trial_demos = db.query(
            Demo
        ).join(
            Client
        ).filter(
            Demo.trial_status == "active",
            Demo.trial_expiry_date != None,
            Demo.trial_expiry_date >= today,
            Demo.trial_expiry_date <= next_15_days
        ).all()

        for demo in trial_demos:

            reminders.append({
                "reminder_type": "Trial Expiry",
                "client_id": demo.client_id,
                "client_name": demo.client.pharmacy_name,
                "reminder_date": demo.trial_expiry_date,
                "status": "Active"
            })

        deals = db.query(
            Deal
        ).join(
            Client
        ).filter(
            Deal.renewal_status == "active",
            Deal.renewal_reminder_date != None,
            Deal.renewal_reminder_date >= today,
            Deal.renewal_reminder_date <= next_30_days
        ).all()

        for deal in deals:

            reminders.append({
                "reminder_type": "Renewal",
                "client_id": deal.client_id,
                "client_name": deal.client.pharmacy_name,
                "reminder_date": deal.renewal_reminder_date,
                "status": "Active"
            })

    reminders.sort(
        key=lambda x: x["reminder_date"]
    )

    return reminders

def get_call_logs_by_client(
    db,
    client_id
):

    return db.query(
        CallLog
    ).filter(
        CallLog.client_id == client_id
    ).order_by(
        CallLog.created_date,
        CallLog.created_time
    ).all()