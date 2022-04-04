import asyncio
from time import perf_counter
from loader import *
from onlinetests.skysmart.skysmart import SkySmartAnswer

if __name__ == "__main__":
	asyncio.get_event_loop().run_until_complete(init_db())
	t1 = perf_counter()
	answer = SkySmartAnswer("biloluregi")
	asyncio.get_event_loop().run_until_complete(answer.get_answers())
	print(
		f"""
Done in {round(perf_counter() - t1, 2)}		
"""
	)