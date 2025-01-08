from typing import Any
from sqlalchemy.orm import Mapped
from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    username: Mapped[str] = Column(String, unique=True, index=True)
    email: Mapped[str] = Column(String, unique=True, index=True)
    hashed_password: Any = Column(String)
    is_active: Mapped[bool] = Column(Boolean, default=True)


#models are how the data are stored and organized in the database, it describes the