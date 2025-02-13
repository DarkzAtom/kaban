from typing import Any
from sqlalchemy.orm import Mapped
from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    title: Mapped[str] = Column(String, unique=True, index=True)
    date: Mapped[str] = Column(String, index=True)
    author: Mapped[str] = Column(String)
    shortdesc: Mapped[str] = Column(String)
    fulldesc: Mapped[str] = Column(String)
    picurl: Mapped[str] = Column(String)

class BbcUrl(Base):
    __tablename__ = "bbc_urls"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    url: Mapped[str] = Column(String, unique=True, index=True)
    processed: Mapped[bool] = Column(Boolean, default=False)