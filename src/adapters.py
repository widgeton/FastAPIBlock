from typing import Sequence
import datetime as dt

from models import TradingResults
from schemas import DynamicTrading, SimpleTrading


class TradingModelAdapter:
    @staticmethod
    def to_dynamic_trading(trading: TradingResults,
                           start: dt.date,
                           end: dt.date
                           ) -> DynamicTrading:
        return DynamicTrading(oil_id=trading.oil_id,
                              delivery_type_id=trading.delivery_type_id,
                              delivery_basis_id=trading.delivery_basis_id,
                              start_date=start,
                              end_date=end)

    @classmethod
    def to_dynamic_trading_list(cls,
                                tradings: Sequence[TradingResults],
                                start: dt.date,
                                end: dt.date
                                ) -> list[DynamicTrading]:
        return [cls.to_dynamic_trading(t, start, end) for t in tradings]

    @staticmethod
    def to_simple_trading(trading: TradingResults) -> SimpleTrading:
        return SimpleTrading(oil_id=trading.oil_id,
                             delivery_type_id=trading.delivery_type_id,
                             delivery_basis_id=trading.delivery_basis_id)

    @classmethod
    def to_simple_trading_list(cls, tradings: Sequence[TradingResults]) -> list[SimpleTrading]:
        return [cls.to_simple_trading(t) for t in tradings]
