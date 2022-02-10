from bs4 import BeautifulSoup

from skysmart_api import SkySmartApi


class SkySmartAnswer:
	def __init__(self, task_hash):
		self.api = SkySmartApi(task_hash)
	
	async def get_answers(self):
		pass

	def get_question(self, soup):
		return soup.find("vim-instruction")

	def math_input_answer(self, soup):
		final_answer = {"type" : "math_input_answer", "question" : self.get_question(soup), "answers" : []}
		for answer in soup.find_all("math-input-answer"):
			final_answer["answers"].append(answer.get_text().strip("\n"))
		return final_answer

	def group_drag_and_drop(self, soup):
		final_answer = {"type" : "group_drag_and_drop", "question" : self.get_question(soup), "answers" : []}
		for group in soup.find_all("vim-dnd-group-item"):
			elements = []
			for answer_id in group.get("drag-ids").split(','):
				elements.append(soup.find("vim-dnd-group-drag", **{"answer-id" : answer_id}).get_text().strip("\n"))
			final_answer["answers"].append({"group" : group.get_text().strip('\n'), "elements" : elements})
		return final_answer

	def test_answer(self, soup):
		final_answer = {"type" : "test_answer", "question" : self.get_question(soup), "answers" : []}
		for answer in soup.find_all("vim-test-item", correct = "true"):
			final_answer["answers"].append(answer.get_text().strip("\n"))
		return final_answer

	def image_drag_and_drop(self, soup):
		final_answer = {"type" : "image_drag_and_drop", "question" : self.get_question(soup), "answers" : []}
		for answer in soup.find_all("vim-dnd-image-set-drag"):
			final_answer["answers"].append(answer.get_text().strip("\n"))
		return final_answer

	def groups_answer(self, soup):
		final_answer = {"type" : "groups_answer", "question" : self.get_question(soup), "answers" : []}
		groups_items_list = soup.find_all("vim-groups-item")
		for i in range(0, len(groups_items_list), 2):
			first_answer = self.decode_base64(groups_items_list[i].get_text()).strip("\n")
			second_answer = self.decode_base64(groups_items_list[i+1].get_text()).strip("\n")
			final_answer["answers"].append(f"{first_answer} - {second_answer}")
		return final_answer

	def strike_out_answer(self, soup):
		final_answer = {"type" : "strike_out_answer", "question" : self.get_question(soup), "answers" : []}
		for answer in soup.find_all("vim-strike-out-item", striked = "true"):
			final_answer["answers"].append(answer.get_text().strip("\n"))
		return final_answer
	
	def input_answer(self, soup):
		final_answer = {"type" : "input_answer", "question" : self.get_question(soup), "answers" : []}
		for answer in soup.find_all("vim-input-item"):
			final_answer["answers"].append(answer.get_text().strip("\n"))
		return final_answer

	def image_answer(self, soup):
		final_answer = {"type" : "image_answer", "question" : self.get_question(soup), "answers" : []}
		for image_group_tag in soup.find_all("vim-test-image"):
			count = 1
			for answer in image_group_tag:
				if type(answer) is bs4.element.NavigableString:
					continue
				if answer.has_attr('correct'):
					final_answer["answers"].append(f"Изображение №{count}")
				count += 1
		return final_answer

	def select_answer(self, soup):
		final_answer = {"type" : "select_answer", "question" : self.get_question(soup), "answers" : []}
		for answer in soup.find_all("vim-select-item", correct = "true"):
			final_answer["answers"].append(answer.get_text().strip("\n"))
		return final_answer
	
	def drag_and_drop(self, soup):
		final_answer = {"type" : "drag_and_drop", "question" : self.get_question(soup), "answers" : []}
		for answer in soup.find_all("vim-dnd-text-drag"):
			final_answer["answers"].append(answer.get_text().strip("\n"))
		return final_answer