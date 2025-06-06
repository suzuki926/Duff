from sqlmodel import SQLModel, Field
from typing import Optional

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    material: str
    manufacturing_place: str
    supply_chain_history: str
    recycling_info: str
