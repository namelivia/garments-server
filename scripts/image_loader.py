import os
from app.database import engine, Base
from app.dependencies import get_db
from app.garments import crud
import requests

Base.metadata.create_all(bind=engine)
db = next(get_db())

all_garments = crud.get_garments(db)
for garment in all_garments:
    id = garment.id
    print(f"The id is :{id}")
    print(f"Does {id}.png exist?")
    try:
        with open(f"images/{id}.png", "rb") as f:
            print("YES")
            print("Uploading image")
            response = requests.post(
                url=os.getenv("IMAGES_SERVICE_ENDPOINT") + "/image",
                files={"media": f.read()},
            )
            print(response.text)
            location = response.headers["location"]
            garment.image = location
            db.commit()
            print(location)
    except IOError:
        print("It does not exist")

    name = garment.name
    print(f"The name is :{name}")
    print(f"Does {name}.png exist?")
    try:
        with open(f"images/{id}.png", "rb") as f:
            print("YES")
            print("Uploading image")
            response = requests.post(
                url=os.getenv("IMAGES_SERVICE_ENDPOINT") + "/image",
                files={"media": f.read()},
            )
            print(response.text)
            location = response.headers["location"]
            garment.image = location
            db.commit()
            print(location)
    except IOError:
        print("It does not exist")
