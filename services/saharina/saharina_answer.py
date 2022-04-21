import aiohttp
from bs4 import BeautifulSoup, element
from .saharina_api import SaharinaApi

class SaharinaAnswer:
	def __init__(self, url: str):
		self.api = SaharinaApi(url)

	@staticmethod
	def __get_task_question(task: element.Tag) -> str:
		raw_question: str = task.find("div", class_ = "task check").get_text()
		return raw_question[1:]

	@staticmethod
	def __get_task_answer(task: element.Tag) -> str:
		raw_answer: element.Tag = task.find("div", class_ = "answers-true")
		return raw_answer.find("span", class_ = "answer").get_text()

	async def get_answers(self) -> list[dict]:
		answers: list[dict] = []
		async with aiohttp.ClientSession() as session:
			html: str = await self.api.get_tasks_html(session)

		soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
		for task in soup.find_all("div", class_ = "task-container"):

			if not task.find("div", class_ = "answers-container"):
				continue
			answer = {
				"question" : self.__get_task_question(task),
				"answer" : self.__get_task_answer(task)
			}
			answers.append(answer)
		return answers



			


		

			


		
