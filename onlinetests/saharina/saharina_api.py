from bs4 import BeautifulSoup
import aiohttp
from onlinetests.exceptions import *


class SaharinaApi:
	def __init__(self, url: str):
		self.url: str = url

	@staticmethod
	def __get_token(soup: BeautifulSoup) -> str:
		token: list = soup.find_all("input", {"name" : "token"})
		if token:
			return token[0]["value"]
		else:
			raise UnknownTestException()

	@staticmethod
	async def __get_tasks_name(soup: BeautifulSoup) -> list[str]:
		tasks: list = []

		for task in soup.find_all("input"):
			task_name = task.get("name")

			if task_name == "token":
				continue
			elif task_name == "searchid":
				break
			
			tasks.append(task_name)

		return tasks

	async def get_html(self, session: aiohttp.ClientSession) -> str:
		
		async with session.get(self.url) as responce:
			html: str = await responce.text()

		soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
		payload: dict = {
			"token" : self.__get_token(soup),
		}
		for task_name in await self.__get_tasks_name(soup):
			payload[task_name] = "1"

		async with session.post(self.url, data=payload) as responce:
			return await responce.text()