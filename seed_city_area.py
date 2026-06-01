import pandas as pd

from database import SessionLocal
from models import City, Area

db = SessionLocal()

file_path = "Book1.xlsx"

df = pd.read_excel(file_path)

for _, row in df.iterrows():

    city_name = str(row["City"]).strip()

    area_name = str(row["Area"]).strip()

    city = db.query(
        City
    ).filter(
        City.name == city_name
    ).first()

    if not city:

        city = City(
            name=city_name
        )

        db.add(city)

        db.commit()
        
        db.close()

        db.refresh(city)

    area = db.query(
        Area
    ).filter(
        Area.name == area_name,
        Area.city_id == city.id
    ).first()

    if not area:

        db.add(
            Area(
                name=area_name,
                city_id=city.id
            )
        )

db.commit()

print("Cities and Areas Imported Successfully")