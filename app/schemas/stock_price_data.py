from pydantic import BaseModel
from typing import Optional


class StockPriceInputData(BaseModel):
    stock_code: str
    start_date: str
    end_date: str
    interval: str
    start_hour: Optional[int] = None
    end_hour: Optional[int] = None


class StockPriceOutputData(BaseModel):
    stock_code: str
    start_date: str
    end_date: str
    interval: str
    start_hour: Optional[int] = None
    end_hour: Optional[int] = None
    # current price
    price: float
    highest: float
    lowest: float
    trend: float
