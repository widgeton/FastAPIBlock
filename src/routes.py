from fastapi import APIRouter
from fastapi_cache.decorator import cache

from repository import TradingRepository
from adapters import TradingModelAdapter
import datetime as dt
from schemas import DynamicTrading, SimpleTrading

router = APIRouter(prefix="", tags=["Tradings"])


@router.get("/get_last_trading_dates", response_model=list[dt.date])
@cache()
async def get_last_trading_dates(amount: int):
    result = await TradingRepository.get_last_trading_dates(amount)
    return result


@router.get("/get_dynamics", response_model=list[DynamicTrading] | dict)
@cache()
async def get_dynamics(start: dt.date, end: dt.date):
    if start > end:
        return {"details": "Start date can't be more then end date."}
    tradings = await TradingRepository.get_tradings_by_date_range(start, end)
    dynamic_tradings = TradingModelAdapter.to_dynamic_trading_list(tradings, start, end)
    return dynamic_tradings


@router.get("/get_trading_results", response_model=list[SimpleTrading])
@cache()
async def get_trading_results(limit: int):
    tradings = await TradingRepository.get_last_trading_results(limit)
    results = TradingModelAdapter.to_simple_trading_list(tradings)
    return results
