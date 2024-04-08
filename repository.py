import datetime as dt
from sqlalchemy import select
from typing import Sequence

from db import async_session_factory
from models import TradingResults


class TradingRepository:
    @staticmethod
    async def get_last_trading_dates(amount: int) -> list[dt.date]:
        async with async_session_factory() as session:
            query = (
                select(TradingResults.date)
                .group_by(TradingResults.date)
                .order_by(TradingResults.date.desc())
                .limit(amount)
            )
            result = await session.execute(query)
            tradings = result.scalars().all()
            return tradings

    @staticmethod
    async def get_tradings_by_date_range(start: dt.date, end: dt.date) -> Sequence[TradingResults]:
        async with async_session_factory() as session:
            query = (
                select(TradingResults)
                .filter(TradingResults.date.between(start, end))
            )
            result = await session.execute(query)
            tradings = result.scalars().all()
            return tradings

    @staticmethod
    async def get_last_trading_results(limit: int) -> Sequence[TradingResults]:
        async with async_session_factory() as session:
            query = (
                select(TradingResults)
                .order_by(TradingResults.date.desc())
                .limit(limit)
            )
            result = await session.execute(query)
            tradings = result.scalars().all()
            return tradings
