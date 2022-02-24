from base64 import b64decode

import aiohttp
from bs4 import BeautifulSoup, element

from onlinetests.skysmart.skysmart_api import SkySmartApi


class SkySmartAnswer:
	def __init__(self, task_hash: str):
		self.api = SkySmartApi(task_hash)

	@staticmethod
	def get_question(soup: BeautifulSoup) -> str:
		return soup.find("vim-instruction").get_text()

	def get_task_answer(self, soup: BeautifulSoup) -> dict:
		answers: list = []
		if soup.find_all("vim-dnd-text-drags"):
			answers += self.drag_and_drop(soup)

		if soup.find_all("vim-select-answers"):
			answers += self.select_answer(soup)

		if soup.find_all("vim-test-image"):
			answers += self.image_answer(soup)

		if soup.find_all("vim-input-answers"):
			answers += self.input_answer(soup)

		if soup.find_all("vim-strike-out"):
			answers += self.strike_out_answer(soup)

		if soup.find_all("vim-groups"):
			answers += self.groups_answer(soup)

		if soup.find_all("vim-dnd-image-set-drags"):
			answers += self.image_drag_and_drop(soup)

		if soup.find_all("vim-test"):
			answers += self.test_answer(soup)

		if soup.find_all("vim-dnd-group"):
			answers += self.group_drag_and_drop(soup)

		if soup.find_all("math-input"):
			answers += self.math_input_answer(soup)

		return {"question": self.get_question(soup), "answers": answers}

	async def get_answers(self):
		answers: list = []
		async with aiohttp.ClientSession() as session:
			auth_token: str = await self.api.auth(session)
			for uuid in await self.api.get_uuids(session, auth_token):
				html: str = await self.api.get_step_html(session, auth_token, uuid)
				answers.append(self.get_task_answer(BeautifulSoup(html, 'html.parser')))
		return answers

	@staticmethod
	def math_input_answer(soup: BeautifulSoup) -> list:
		answers: list = []
		for answer in soup.find_all("math-input-answer"):
			answers.append(answer.get_text().strip("\n"))
		return answers

	@staticmethod
	def group_drag_and_drop(soup: BeautifulSoup) -> list:
		answers: list = []

		for group in soup.find_all("vim-dnd-group-item"):
			elements: list = []
			group_name: str = group.get_text().strip('\n')
			for answer_id in group.get("drag-ids").split(','):
				group_element: str = soup.find("vim-dnd-group-drag", attrs={"answer-id": answer_id}).get_text()
				elements.append(group_element.strip("\n"))
			answer = {"group": group_name, "elements": elements}
			answers.append(answer)

		return answers

	@staticmethod
	def test_answer(soup: BeautifulSoup) -> list:
		answers: list = []
		for answer in soup.find_all("vim-test-item", correct="true"):
			answers.append(answer.get_text().strip("\n"))
		return answers

	@staticmethod
	def image_drag_and_drop(soup: BeautifulSoup) -> list:
		answers: list = []
		for answer in soup.find_all("vim-dnd-image-set-drag"):
			answers.append(answer.get_text().strip("\n"))
		return answers

	@staticmethod
	def groups_answer(soup: BeautifulSoup) -> list:
		answers: list = []
		groups_items_list = soup.find_all("vim-groups-item")
		for i in range(0, len(groups_items_list), 2):
			first_answer: str = b64decode(groups_items_list[i].get_text()).decode("utf-8").strip("\n")
			second_answer: str = b64decode(groups_items_list[i + 1].get_text()).decode("utf-8").strip("\n")
			answers.append(f"{first_answer} - {second_answer}")
		return answers

	@staticmethod
	def strike_out_answer(soup: BeautifulSoup) -> list:
		answers: list = []
		for answer in soup.find_all("vim-strike-out-item", striked="true"):
			answers.append(answer.get_text().strip("\n"))
		return answers

	@staticmethod
	def input_answer(soup: BeautifulSoup) -> list:
		answers: list = []
		for answer in soup.find_all("vim-input-item"):
			answers.append(answer.get_text().strip("\n"))
		return answers

	@staticmethod
	def image_answer(soup: BeautifulSoup) -> list:
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
	def select_answer(soup: BeautifulSoup) -> list:
		answers: list = []
		for answer in soup.find_all("vim-select-item", correct="true"):
			answers.append(answer.get_text().strip("\n"))
		return answers

	@staticmethod
	def drag_and_drop(soup: BeautifulSoup) -> list:
		answers: list = []
		for answer in soup.find_all("vim-dnd-text-drag"):
			answers.append(answer.get_text().strip("\n"))
		return answers
