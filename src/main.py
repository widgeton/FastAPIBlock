from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from config import settings
from routes import router as trading_router

CACHE_PREFIX = "api:cache"


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix=CACHE_PREFIX)
    yield


app = FastAPI(title="Tradings", lifespan=lifespan)
app.include_router(trading_router)
