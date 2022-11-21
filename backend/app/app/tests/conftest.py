import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.db.base_class import Base
from app.main import app, get_db
from app.core.config import settings

test_engine = create_engine(
    settings.test_db_url,
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
