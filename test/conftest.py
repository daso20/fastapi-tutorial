from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
#from alembic import command

#SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:appliance@localhost:5432/fastapi_test}'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #command.upgrade("head")    # Not tested (Alembic)
    #command.downgrade("head")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def overrride_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrride_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user