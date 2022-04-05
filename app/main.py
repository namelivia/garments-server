from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.garments.api import router as garments
from app.places.api import router as places
from app.activities.api import router as activities
from app.images.api import router as images
from app.users.api import router as users
from app.garment_types.api import router as garment_types
import logging
import sys

app = FastAPI()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

origins = ["http://localhost:3000", "http://garments.namelivia.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

[
    app.include_router(router)
    for router in [
        garments,
        places,
        activities,
        images,
        users,
        garment_types,
    ]
]
