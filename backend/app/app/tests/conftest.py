import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.core.config import settings
from app.main import app
from app.db.base_class import Base
from app.api.deps import get_db

test_engine = create_engine(
    settings.TEST_DB_URL,
    connect_args={'check_same_thread': False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(scope='function')
def client():
    with TestClient(app) as client:
        Base.metadata.create_all(bind=test_engine)
        try:
            yield client
        finally:
            Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope='function')
def user():
    return {
        'full_name': 'John Doe',
        'password': 'password',
    }
