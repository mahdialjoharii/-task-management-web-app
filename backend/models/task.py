from sqlalchemy import Column, Date, ForeignKey, Integer, String
from database.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    status = Column(String, nullable=False, default="TODO")
    due_date = Column(Date, nullable=True)