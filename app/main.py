from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

## Usage of ORM
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import Settings

## Alembic 
from alembic import command
from alembic.config import Config

## No longer required as alembic creates all of the tables
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

## Restricted origin list
#origins = ["https://www.google.com"]

origins = ["*"] ## Everyone

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message":"Hello world!!!"}

# Alembic startup function
def run_alembic_upgrade():
    alembic_cfg = Config("alembic.ini") 
    command.upgrade(alembic_cfg, "head")

# Define a startup event handler using a lifespan event
def on_startup():
    run_alembic_upgrade()

app.add_event_handler("startup", on_startup)