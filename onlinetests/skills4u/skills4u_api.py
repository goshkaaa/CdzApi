import re
import json
import asyncio

import aiohttp
from bs4 import BeautifulSoup, element

from onlinetests.exceptions import *


class Skills4uApi:
	def __init__(self, url):
		self.url: str = url

	async def get_json(self, session: aiohttp.ClientSession) -> dict:
		script: str = await self.__get_tasks_script(session)
		json_answers: str = re.findall(r"\[{.*}\]", script)[0]
		return json.loads(json_answers)

	async def __get_tasks_script(self, session: aiohttp.ClientSession) -> str:
		
		async with session.get(self.url) as responce:
			html: str = await responce.text()

		soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
		container: element.Tag = soup.find("div", class_ = "container")
		scripts: list = container.find_all("script")

		if len(scripts) < 1 or not "window.lesson" in str(scripts[1]):
			raise Exception("Site structure has been changed!")
		else:
			return str(scripts[1])