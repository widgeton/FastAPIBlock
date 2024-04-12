import datetime as dt
import pytest

from repository import TradingRepository
from models import TradingResults


@pytest.mark.asyncio(scope="session")
async def test_get_last_trading_dates():
    dates = await TradingRepository.get_last_trading_dates(2)
    assert dates == [dt.date(year=2024, month=4, day=4),
                     dt.date(year=2024, month=3, day=25)]


@pytest.mark.asyncio(scope="session")
async def test_get_tradings_by_date_range(tradings):
    trds = await TradingRepository.get_tradings_by_date_range(dt.date(year=2024, month=2, day=28),
                                                              dt.date(year=2024, month=3, day=26))
    assert trds == [TradingResults(**tradings[0]), TradingResults(**tradings[2])]


@pytest.mark.asyncio(scope="session")
async def test_get_last_trading_results(tradings):
    res = await TradingRepository.get_last_trading_results(1)
    assert res == [TradingResults(**tradings[1])]
