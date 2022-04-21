import asyncio
from time import perf_counter
from loader import *
from services import SkySmartAnswer
import aiohttp

async def main():
	await init_db()
	t1 = perf_counter()
	answer = SkySmartAnswer("biloluregi")
	print(await answer.get_answers())
	print(
		f"""
Done in {round(perf_counter() - t1, 2)}		
"""
	)


asyncio.get_event_loop().run_until_complete(main())