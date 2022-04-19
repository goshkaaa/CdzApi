import asyncio
from time import perf_counter
from loader import *
from onlinetests.skysmart.skysmart import SkySmartAnswer
from onlinetests.lecta.lecta import LectaAnswer
import aiohttp

async def main():
	await init_db()
	t1 = perf_counter()
	answer = LectaAnswer("hidinexega")
	print(await answer.get_answers())
	print(
		f"""
Done in {round(perf_counter() - t1, 2)}		
"""
	)
	answer = SkySmartAnswer("biloluregi")
	print(await answer.get_answers())

asyncio.get_event_loop().run_until_complete(main())