import aioredis
import asyncio
from urllib.parse import urlparse
from api_variables import services
import os

async def check_auth_token(token):
    possible_token = await redis.get(token)
    
    if possible_token == None: # если такой записи не существует
        return False

    if possible_token == b"token": # если эта запись - не токен
        return True

    return False

async def solve_any_test(url):
    service = await get_service(url)

async def get_service(url) -> str:
    result = services.get(urlparse(url).netloc)

    if not result:
        return False

    return result

async def init_redis() -> None:
    global redis
    
    redis_ip = os.environ.get("redis_ip")
    redis_password = os.environ.get("redis_password")

    redis = await aioredis.from_url(
        f"redis://{redis_ip}",
        password=redis_password,
    )