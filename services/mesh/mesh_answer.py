import aiohttp
import json
from .mesh_api import MeshApi

class MeshAnswer:
	def __init__(self, test_type: str, test_variant: str):
		self.api = MeshApi(test_type, test_variant)

	@staticmethod
	def __get_question(task: dict) -> dict:
		question: dict = {"text" : "", "image_url" : ""}
		for que_entry in task["test_task"]["question_elements"]:
			if que_entry["type"] == "content/text":
				question["text"] += que_entry["text"] + " "
			elif que_entry["type"] == "content/atomic":
				if que_entry["atomic_type"] == "image":
					question["image_url"] += f'https://uchebnik.mos.ru/cms{que_entry["preview_url"]}'
				else:
					question["image_url"] += que_entry["preview_url"]
		return question


	@staticmethod
	def __single_answer(answer_info: dict) -> list[str]:
		answer_id: str = answer_info["right_answer"]["id"]
		for entry in answer_info["options"]:
			if entry["id"] == answer_id: 
				if entry["text"]:
					return [entry["text"]]
				return [entry["content"][0]["content"]]

	@staticmethod
	def __string_answer(answer_info: dict) -> list[str]:
		return [answer_info["right_answer"]["string"]]

	@staticmethod
	def __order_answer(answer_info: dict) -> list[str]:
		answers: list = []
		order_ids: list = answer_info["right_answer"]["ids_order"]
		for correct_element in order_ids:
			for answer_entry in answer_info["options"]:
				if answer_entry["id"] == correct_element:
					if answer_entry["text"]:
						answers.append(answer_entry["text"])
					else:
						answers.append(answer_entry["content"][0]["content"])
		return answers

	@staticmethod
	def __groups_answer(answer_info: dict) -> list[dict]:
		answers: list = []
		correct_groups: dict = answer_info["right_answer"]["groups"]
		for group in correct_groups:
			group_name: str
			group_elements: list = []

			for answer_entry in answer_info["options"]:
				if answer_entry["id"] == group["group_id"]:
					if answer_entry["text"]:
						group_name = answer_entry["text"]
					else:
						group_name = answer_entry["content"][0]["content"]
				elif answer_entry["id"] in group["options_ids"]:
					if answer_entry["text"]:
						group_elements.append(answer_entry["text"])
					else:
						group_elements.append(answer_entry["content"][0]["content"])

			answers.append({"group_name" : group_name, "group_elements" : group_elements})
		
		return answers

	@staticmethod
	def __multiple_answer(answer_info: dict) -> list[str]:
		answers: list = []
		answer_ids: list = answer_info["right_answer"]["ids"]
		for answer_id in answer_ids:
			for answer_entry in answer_info["options"]:
				if answer_entry["id"] == answer_id:
					if answer_entry["text"]:
						answers.append(answer_entry['text'])
					else:
						answers.append(answer_entry['content'][0]['content'])
		return answers

	@staticmethod
	def __single_choice_answer(answer_info: dict) -> list[str]:
		answers: list = []
		answer_ids: list = answer_info["right_answer"]["text_position_answer"]
		for field_num, answer_id in enumerate(answer_ids):
			entry_options: list = answer_info["text_position"][field_num]["options"]

			for entry in entry_options:
				if entry["id"] == answer_id["id"]:
					if entry["text"]:
						answers.append(entry["text"])
					else:
						answers.append(entry['content'][0]['content'])
		return answers

	@staticmethod
	def __number_answer(answer_info: dict) -> list[str]:
		return [str(answer_info["right_answer"]["number"])]

	@staticmethod
	def __gap_match_answer(answer_info: dict) -> list[str]:
		answers: list = []
		answer_ids: list = answer_info["right_answer"]["text_position_answer"]
		for answer_id in answer_ids:
			for answer_option in answer_info["options"]:
				if answer_id["id"] == answer_option["id"]:
					if answer_option['text']:
						answers.append(answer_option['text'])
					else:
						answers.append(answer_option['content'][0]['content'])
		return answers

	@staticmethod
	def __match_answer(answer_info: dict) -> list[dict]:
		answers: list = []
		correct_elements: dict = answer_info["right_answer"]["match"]
		for key, value in correct_elements.items():
			key_name: str = ""
			value_name: str = ""
			image_url = None 
			for answer_entry in answer_info["options"]:
				if answer_entry["id"] == key:
					if answer_entry["text"]:
						key_name = answer_entry["text"]
					elif answer_entry["content"][0]["type"] == "content/atomic":
						key_name = answer_entry["content"][0]["relative_url"]
					else:
						image_url = answer_entry["content"][0]["content"]
				elif answer_entry["id"] == value[0]:
					if answer_entry["text"]: 
						value_name = answer_entry["text"]
					else:
						value_name = answer_entry["content"][0]["content"]
			answers.append({"key" : key_name, "value" : value_name, "image_url" : image_url})
		return answers