import re
import json

import aiohttp

from onlinetests.skills4u.skills4u_api import Skills4uApi

class Skills4uAnswer:
	def __init__(self, url):
		self.api = Skills4uApi(url)

	@staticmethod
	def __clean_string(string: str):
		string = string.replace("`", "")
		pattern = re.compile('<.*?>')
		return re.sub(pattern, "", string)

	async def get_answers(self):
		answers: list = []
		async with aiohttp.ClientSession() as session:
			answers_json: dict = await self.api.get_json(session)	
			
		for task in answers_json:
			answer = {
				"question" : self.__clean_string(task["question"]),
				"answer" : self.__clean_string(task["answer"])
			}
			answers.append(answer)
		
		return answers