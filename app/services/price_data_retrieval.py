import pandas as pd
from app.schemas.stock_price_data import StockPriceInputData, StockPriceOutputData
from trade_assistant.consts import StockTable
from trade_assistant.database.db_pool import DataBasePool
from fastapi import Depends
import asyncpg


class PriceDataRetriever:
    # Table
    TABLE_NAME_5M = StockTable.STOCK_5M_INFO
    TABLE_NAME_EOD = StockTable.STOCK_EOD_INFO
    # Fields
    TRADING_DATE = "trading_date"
    CREATED_AT = "created_at"
    CLOSE = "close"
    HIGH = "high"
    LOW = "low"
    VOLUME = "volume"
    SYMBOL = "ticker"

    def __init__(self, retriever: asyncpg.Pool = Depends(DataBasePool.get_pool)):
        self.retriever = retriever

    async def _retrieve_5m(self, input_data: StockPriceInputData):
        query = f"""
            SELECT 
                {self.TRADING_DATE}, 
                {self.CREATED_AT},
                {self.CLOSE},
                {self.HIGH},
                {self.LOW},
                {self.VOLUME}
            FROM {self.TABLE_NAME_5M}
            WHERE
                {self.SYMBOL} = '{input_data.stock_code}'
                AND {self.TRADING_DATE} >= '{input_data.start_date}'
                AND {self.TRADING_DATE} <= '{input_data.end_date}'
                AND cast(extract(hour from to_timestamp({self.CREATED_AT})) as int) >= {input_data.start_hour}
                AND cast(extract(hour from to_timestamp({self.CREATED_AT})) as int) <= {input_data.end_hour}
        """
        async with self.retriever.acquire() as connection:
            async with connection.transaction():
                # do something with the db_pool
                result = await connection.fetch(query)

        return pd.DataFrame([dict(row) for row in result])

    async def _retrieve_eod(self, input_data: StockPriceInputData):
        query = f"""
            SELECT 
                {self.TRADING_DATE}, 
                {self.CREATED_AT},
                {self.CLOSE},
                {self.HIGH},
                {self.LOW},
                {self.VOLUME}
            FROM {self.TABLE_NAME_EOD}
            WHERE
                {self.SYMBOL} = '{input_data.stock_code}'
                AND {self.TRADING_DATE} >= '{input_data.start_date}'
                AND {self.TRADING_DATE} <= '{input_data.end_date}'
        """
        async with self.retriever.acquire() as connection:
            async with connection.transaction():
                # do something with the db_pool
                result = await connection.fetch(query)

        return pd.DataFrame([dict(row) for row in result])

    async def retrieve(self, input_data: StockPriceInputData) -> StockPriceOutputData:
        if input_data.interval == "5m":
            df = await self._retrieve_5m(input_data)
        elif input_data.interval == "eod":
            df = await self._retrieve_eod(input_data)
        else:
            raise ValueError(f"Unknown interval: {input_data.interval}")
        return StockPriceOutputData(
            stock_code=input_data.stock_code,
            start_date=input_data.start_date,
            end_date=input_data.end_date,
            interval=input_data.interval,
            start_hour=input_data.start_hour,
            end_hour=input_data.end_hour,
            price=df[self.CLOSE].iloc[-1],
            highest=df[self.HIGH].max(),
            lowest=df[self.LOW].min(),
            trend=100 * (df[self.CLOSE].iloc[-1] / df[self.CLOSE].iloc[0] - 1)
        )
