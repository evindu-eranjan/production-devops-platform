from sqlalchemy import Column, Integer, String, Boolean, Text

from app.database import Base


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)