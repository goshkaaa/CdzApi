import asyncio

from onlinetests.skysmart.skysmart import SkySmartAnswer

if __name__ == "__main__":
	answer = SkySmartAnswer("ximenasiru")
	asyncio.run(answer.get_answers())