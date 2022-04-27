import asyncio
from time import perf_counter
from .loader import *
from .services import SkySmartAnswer
import aiohttp

async def main(url):
	await init_db()
	answer = SkySmartAnswer(url.split("https://edu.skysmart.ru/student/")[1])
	data = (await answer.get_answers())

	return data 