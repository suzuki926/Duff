from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import uuid4
from datetime import datetime

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    material: str
    manufacturing_place: str
    supply_chain_history: str
    recycling_info: str


class RequestURL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(foreign_key="request.id")
    url: str = Field(default_factory=lambda: str(uuid4()))
    tier: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    request: Optional["Request"] = Relationship(back_populates="urls")


class Request(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    tier: int = 1
    urls: List[RequestURL] = Relationship(back_populates="request")


class RequestCreate(SQLModel):
    content: str


class RequestURLRead(SQLModel):
    id: int
    url: str
    tier: int
    created_at: datetime


class RequestRead(SQLModel):
    id: int
    content: str
    tier: int
    urls: List[RequestURLRead] = []
