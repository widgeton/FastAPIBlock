import datetime as dt
from pydantic import BaseModel


class SimpleTrading(BaseModel):
    oil_id: str
    delivery_type_id: str
    delivery_basis_id: str


class DynamicTrading(SimpleTrading):
    start_date: dt.date
    end_date: dt.date
