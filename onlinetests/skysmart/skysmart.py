from base64 import b64decode

import aiohttp
from bs4 import BeautifulSoup, element

from onlinetests.skysmart.skysmart_api import SkySmartApi


class SkySmartAnswer:
	def __init__(self, task_hash: str):
		self.api = SkySmartApi(task_hash)

	@staticmethod
	def __get_question(soup: BeautifulSoup) -> str:
		return soup.find("vim-instruction").get_text()

	def __get_task_answer(self, soup: BeautifulSoup) -> dict[str, list]:
		answers: list = []
		if soup.find_all("vim-dnd-text-drags"):
			answers += self.__drag_and_drop(soup)

		if soup.find_all("vim-select-answers"):
			answers += self.__select_answer(soup)

		if soup.find_all("vim-test-image"):
			answers += self.__image_answer(soup)

		if soup.find_all("vim-input-answers"):
			answers += self.__input_answer(soup)

		if soup.find_all("vim-strike-out"):
			answers += self.__strike_out_answer(soup)

		if soup.find_all("vim-groups"):
			answers += self.__groups_answer(soup)

		if soup.find_all("vim-dnd-image-set-drags"):
			answers += self.__image_drag_and_drop(soup)

		if soup.find_all("vim-test"):
			answers += self.__test_answer(soup)

		if soup.find_all("vim-dnd-group"):
			answers += self.__group_drag_and_drop(soup)

		if soup.find_all("math-input"):
			answers += self.__math_input_answer(soup)

		return {
			"question": self.__get_question(soup), 
			"answers": answers
		}

	async def get_answers(self) -> list[dict]: #переписать!
		answers: list = []

		async with aiohttp.ClientSession() as session:
			htmls: list = await self.api.get_htmls(session)
		
		for html in htmls:
			soup: BeautifulSoup = BeautifulSoup(html["content"], "html.parser")
			answers.append(self.__get_task_answer(soup)) 

		return answers

	@staticmethod
	def __math_input_answer(soup: BeautifulSoup) -> list[str]:
		answers: list = []
		for answer in soup.find_all("math-input-answer"):
			answers.append(answer.get_text().strip("\n"))
		return answers

	@staticmethod
	def __group_drag_and_drop(soup: BeautifulSoup) -> list[str]:
		answers: list = []

		for group in soup.find_all("vim-dnd-group-item"):
			answer: str = group.get_text().strip("\n") + ":\n"
			for answer_id in group.get("drag-ids").split(','):
				group_element: str = soup.find("vim-dnd-group-drag", attrs={"answer-id": answer_id}).get_text()
				answer += group_element + "\n"
			answers.append(answer[:-1]) #вырезаем последний \n

		return answers

	@staticmethod
	def __test_answer(soup: BeautifulSoup) -> list[str]:
		answers: list = []
		for answer in soup.find_all("vim-test-item", correct="true"):
			answers.append(answer.get_text().strip("\n"))
		return answers

	@staticmethod
	def __image_drag_and_drop(soup: BeautifulSoup) -> list[str]:
		answers: list = []
		for answer in soup.find_all("vim-dnd-image-set-drag"):
			answers.append(answer.get_text().strip("\n"))
		return answers

	@staticmethod
	def __groups_answer(soup: BeautifulSoup) -> list[str]:
		answers: list = []
		groups_items_list = soup.find_all("vim-groups-item")
		for i in range(0, len(groups_items_list), 2):
			first_answer: str = b64decode(groups_items_list[i].get_text()).decode("utf-8").strip("\n")
			second_answer: str = b64decode(groups_items_list[i + 1].get_text()).decode("utf-8").strip("\n")
			answers.append(f"{first_answer} - {second_answer}")
		return answers

	@staticmethod
	def __strike_out_answer(soup: BeautifulSoup) -> list[str]:
		answers: list = []
		for answer in soup.find_all("vim-strike-out-item", striked="true"):
			answers.append(answer.get_text().strip("\n"))
		return answers

	@staticmethod
	def __input_answer(soup: BeautifulSoup) -> list[str]:
		answers: list = []
		for answer in soup.find_all("vim-input-item"):
			answers.append(answer.get_text().strip("\n"))
		return answers

	@staticmethod
	def __image_answer(soup: BeautifulSoup) -> list[str]:
		answers: list = []
		for image_group_tag in soup.find_all("vim-test-image"):
			count = 1
			for answer in image_group_tag:
				if type(answer) is element.NavigableString:
					continue
				if answer.has_attr('correct'):
					answers.append(f"Изображение №{count}")
				count += 1
		return answers

	@staticmethod
	def __select_answer(soup: BeautifulSoup) -> list[str]:
		answers: list = []
		for answer in soup.find_all("vim-select-item", correct="true"):
			answers.append(answer.get_text().strip("\n"))
		return answers

	@staticmethod
	def __drag_and_drop(soup: BeautifulSoup) -> list[str]:
		answers: list = []
		for answer in soup.find_all("vim-dnd-text-drags"):
			answers.append(answer.get_text().strip("\n").replace("\n", " "))
		return answers
