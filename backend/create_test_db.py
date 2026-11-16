from database.database import engine
from sqlalchemy import create_engine, text

admin_engine = create_engine(
    engine.url.set(database="postgres"),
    isolation_level="AUTOCOMMIT"
)

with admin_engine.connect() as connection:
    exists = connection.execute(text(
        "SELECT 1 FROM pg_database "
        "WHERE datname = 'task_management_test'"
    )).scalar()

    if not exists:
        connection.execute(
            text("CREATE DATABASE task_management_test")
        )
        print("Test database created successfully!")
    else:
        print("Test database already exists!")

admin_engine.dispose()

test_engine = create_engine(
    engine.url.set(database="task_management_test")
)

with test_engine.connect() as connection:
    print("Connected to:", connection.execute(
        text("SELECT current_database()")
    ).scalar())

test_engine.dispose()