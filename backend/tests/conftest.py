
import os

import pytest
from dotenv import load_dotenv
from sqlalchemy.engine import make_url
from sqlalchemy import text
from fastapi.testclient import TestClient

load_dotenv()

database_url = make_url(os.environ["DATABASE_URL"])

test_database_url = database_url.set(
    database="task_management_test"
)

os.environ["DATABASE_URL"] = test_database_url.render_as_string(
    hide_password=False
)

from database.database import Base, engine
from main import app


assert engine.url.database == "task_management_test"


@pytest.fixture(scope="function")
def client():
    with engine.connect() as connection:
        database_name = connection.execute(
            text("SELECT current_database()")
        ).scalar()

        assert database_name == "task_management_test"

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)
