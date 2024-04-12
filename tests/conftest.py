import datetime as dt
import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert
from httpx import AsyncClient, ASGITransport
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache import FastAPICache
from asgi_lifespan import LifespanManager

from config import settings
from db import Base
from models import TradingResults
from routes import router as trading_routes

engine = create_async_engine(settings.DB_URL)


@pytest.fixture
async def app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        FastAPICache.init(InMemoryBackend())
        yield

    app = FastAPI(title="Tradings", lifespan=lifespan)
    app.include_router(trading_routes)

    async with LifespanManager(app) as manager:
        yield manager.app


@pytest.fixture(scope="session")
def tradings() -> list[dict]:
    tradings = [
        {'id': 1,
         'exchange_product_id': 'A100ANK060F',
         'exchange_product_name': 'Бензин (АИ-100-К5), Ангарск-группа станций (ст. отправления)',
         'oil_id': 'A100',
         'delivery_basis_id': 'ANK',
         'delivery_basis_name': 'Ангарск-группа станций',
         'delivery_type_id': 'F',
         'volume': 60,
         'total': 4500000,
         'count': 1,
         'date': dt.date(year=2024, month=2, day=29)},
        {'id': 2,
         'exchange_product_id': 'A100ANK060F',
         'exchange_product_name': 'Бензин (АИ-100-К5), Ангарск-группа станций (ст. отправления)',
         'oil_id': 'A100',
         'delivery_basis_id': 'ANK',
         'delivery_basis_name': 'Ангарск-группа станций',
         'delivery_type_id': 'F',
         'volume': 60,
         'total': 4500000,
         'count': 1,
         'date': dt.date(year=2024, month=4, day=4)},
        {'id': 3,
         'exchange_product_id': 'A100ANK060F',
         'exchange_product_name': 'Бензин (АИ-100-К5), Ангарск-группа станций (ст. отправления)',
         'oil_id': 'A100',
         'delivery_basis_id': 'ANK',
         'delivery_basis_name': 'Ангарск-группа станций',
         'delivery_type_id': 'F',
         'volume': 60,
         'total': 4500000,
         'count': 1,
         'date': dt.date(year=2024, month=3, day=25)}
    ]
    return tradings


@pytest.fixture(scope="session", autouse=True)
async def setup_db(tradings):
    assert settings.MODE == "TEST"
    async with engine.connect() as con:
        await con.run_sync(Base.metadata.drop_all)
        await con.run_sync(Base.metadata.create_all)
        await con.execute(insert(TradingResults), tradings)
        await con.commit()
    yield
    async with engine.connect() as con:
        await con.run_sync(Base.metadata.drop_all)
        await con.commit()


@pytest.fixture
async def client(app):
    async with AsyncClient(base_url="http://test", transport=ASGITransport(app=app)) as client:
        yield client
