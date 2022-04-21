from wsgiref import headers
import aiohttp

import asyncio
from bs4 import BeautifulSoup
import json
import time

test_urs = [
	"https://foxford.ru/trainings/1554",
	"https://foxford.ru/trainings/819",
	"https://foxford.ru/trainings/16225"
]

async def gen_headers(test_id):
	return {
		"Accept": "application/json, text/plain, */*",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
		"Connection": "keep-alive",
		"Cookie" : "uid_updated=1; _sid=c3b8114ab2de43600e8ba9955795b338; _gcl_au=1.1.2018537061.1647298534; client_timezone=Europe/London; _truid=78507f980aa21a5924888c438edf98d0; _ym_uid=1647298537493739381; _ym_d=1647298537; _tm_lt_sid=1647298536600.350836; _foxford_cookie_consent=yes; __exponea_etc__=ccf9bb41-94a4-4112-844b-a67c9f676aeb; uid=1d536b745169b006c6cc304ec5fb8cf6; tmr_lvid=eb273f118838a21653a441f22669e5ab; tmr_lvidTS=1647549027837; _gid=GA1.2.242665190.1647780765; usedesk-widget__login-user-data={%22email%22:%22shootersteam@yandex.ru%22%2C%22phone%22:null%2C%22name%22:%22%D0%98%D1%81%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%20%D0%9D%D0%B5%D0%BE%D0%BF%D0%BE%D0%B7%D0%BD%D0%B0%D0%BD%D0%BD%D1%8B%D0%B9%22%2C%22signature%22:8618741}; tmr_detect=1%7C1647781562083; tmr_reqNum=25; remember_user_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IlcxczROakU0TnpReFhTd2lKREpoSkRFd0pHZHpiQzUyT1VoT2MyZE5OVFpEZWpKdWRHWXZWSFVpTENJeE5qUTROVGcyT1RNeUxqZzROekUyTURnaVhRPT0iLCJleHAiOiIyMDIyLTA2LTI5VDIwOjQ4OjUyWiIsInB1ciI6bnVsbH19--a0882434ce16d3c693c869bed0ce3a172c1a5412; _fox_session=9778428a390d142caff38fe2c13203b2; __exponea_time2__=-1.2686426639556885; _ym_isad=1; _ga=GA1.1.390504727.1647298537; usedesk_messenger_token=8618741; _csrf_token=Qn9gaYu5OOAV5bmWskWkfrhktq8OV2WLfdC7Yl%2FI%2BVOHaNyise9hUCtoUJkemnb%2FCuHECjddVO7oeYgdxAbYfA%3D%3D; _ga_0VQW9WQZ55=GS1.1.1647861229.10.1.1647861652.54",
		"Host": "foxford.ru",
		"If-None-Match": 'W/"0052917cbfa59eb8971e809a7da43f84"',
		"newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMyMDI3NDMiLCJhcCI6IjUxMjY1NzM4OSIsImlkIjoiNjEwYzJlZDkwN2ZkMWFhMSIsInRyIjoiZWQ1ZWM4MTUzYjlmZDAxZDJhMWFkOTFjMTA3NmJkOTAiLCJ0aSI6MTY0NzU0OTA1NjEwNX19",
		f"Referer": "https://foxford.ru/trainings/{test_id}",
		"sec-ch-ua": 'Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
		"sec-ch-ua-mobile": "?0",
		"sec-ch-ua-platform": '"Windows"',
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Site": "same-origin",
		"traceparent": "00-ed5ec8153b9fd01d2a1ad91c1076bd90-610c2ed907fd1aa1-01",
		"tracestate": "3202743@nr=0-1-3202743-512657389-610c2ed907fd1aa1----1647549056105",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
		"X-CSRF-Token": "yN2OkHk1P9Utqs86Jfi0hW4nPaogiSPMUZvehHJmszA9A2GZZ9xkD3FrZ9oaKtNcg3UrxVsp71FFphpPV/y2pA==",
		"X-NewRelic-ID": "VwQHU1FXCxAFVVNUAgYEVlc=",
		"X-Requested-With": "XMLHttpRequest"
	}



async def start_test(test_id, headers):
	url = f"https://foxford.ru/api/trainings/{test_id}/start"
	
	async with aiohttp.ClientSession() as session:
		async with session.post(url, headers=(headers)) as data:
			print( await data.text() )

			if data.status == 200:
				return await data.json()
			return False

async def set_traqtor(id, headers):
	url = "https://foxford.ru/traqtor"
	data = {
		"referrer":"https://foxford.ru/dashboard/daily-plan",
		"href":"https://foxford.ru/catalog/trainings"
	}

	async with aiohttp.ClientSession() as session:
		async with session.post(url, data=(data), headers=headers) as resp:
			print(resp.cookies)
			pass

async def get_test(test_id, headers):
	await set_traqtor(id=test_id, headers=headers)

	url = f"https://foxford.ru/api/trainings/{test_id}"
	
	async with aiohttp.ClientSession() as session:
		async with session.get("https://foxford.ru/api/user/me", headers = headers) as resp:
			print(await resp.text())
		async with session.get(url, headers=(headers)) as data:
			if data.status == 200:
				name = await data.json()
				if name['tasks'] == []:
					return await start_test(test_id, headers)
				return name
			return False

async def get_tasks_ids(data):
	output = []

	for task in data:
		output.append(task['id'])

	return output

async def get_text_gap_response(question):
	output = {}
	q_id = question['id']

	for answer in question['answers']:
		output[f"questions[{q_id}][{answer['id']}]"] = "1"

	return output

async def send_task(uri, data, headers):
	async with aiohttp.ClientSession() as session:
		async with session.post(uri, headers=headers, data=data) as response:
			pass

async def get_radio_response(question):
	return {
		f"questions[{question['id']}]": question['answers'][0]['id']
	}

async def get_checkbox_response(question):
	return {
		f"questions[{question['id']}][]": question['answers'][0]['id']
	}

async def get_links_response(question):
	output = {}
	q_id = question['id']
	c = 0
	free = False
	if len(question['answers']) != len(question['available_answers']):
		free = True
	for answer in question['answers']:
		output[f"questions[{q_id}][{answer['id']}]"] = question['available_answers'][c]['id']
		if not free:
			c+=1

	return output

async def get_text_response(question):
	return {
		f"questions[{question['id']}][]": "1"
	}

async def get_match_group_response(question):
	print(question)
	exit()

async def get_response(question, test_id, task_id, type, headers):

	if type == "text_gap":
		return await get_text_gap_response(question)

	if type == "radio":
		return await get_radio_response(question)
	
	if type == "checkbox":
		return await get_checkbox_response(question)

	if type == "links":
		return await get_links_response(question)

	if type == "text":
		return await get_text_response(question)
	
	print(type)
	return False

async def send_response(data, test_id, task_id, headers):
	uri = f'https://foxford.ru/api/trainings/{test_id}/tasks/{task_id}/answer_attempts'
	final_response = {}

	questions = data['questions']
	for question in questions:
		type = question['type']
		response = await get_response(question, test_id, task_id, type, headers)
		if not response:
			return 0
		final_response = {**final_response, **response}

	await send_task(uri, final_response, headers)



async def submit_answers(tasks, headers, t_id):
	for task in tasks:
		url = f"https://foxford.ru/api/trainings/{t_id}/tasks/{task}"
		print(url)
		async with aiohttp.ClientSession() as session:
			async with session.get(url, headers=(headers)) as data:
				if data.status == 200:
					await send_response(await data.json(), t_id, task, headers)
					#exit()
	
	return True

async def finish_test(id, headers):
	url = f"https://foxford.ru/api/trainings/{id}/finish"
	async with aiohttp.ClientSession() as session:
		async with session.post(url, headers=(headers)) as data:
			if data.status == 200:
				return True
			return False

async def get_radio_answer(question):
	for answer in question['answers']:
		if str(answer['correct']) == "True":
			return "• " + answer['content'] + "<br> "

async def get_links_answer(question):
	output = ""

	for answer in question['answers']:
		for cac in answer['correct_answer_ids']:
			match = ""
			for possible_match in question['available_answers']:
				if str(possible_match['id']) == str(cac):
					if possible_match.get('content'):
						match = possible_match['content']
					if possible_match.get('file_url'):
						match = '<img src="' + possible_match['file_url'] + '">'
					break
			if match != "":
				output += answer['content'] + " → " + match + '<br>'

	return output

async def get_text_answer(question):
	output = ""
	for answer in question['correct_answers']:
		output += "• " + answer + "<br>"

	return output

async def get_text_gap_answer(question):
	output = ""
	#print(question)
	question_data = json.loads(question['editor_content'])
	#print(question_data)

	for task in question_data['document']['nodes']:
		part_text = ""
		for part in task['nodes']:
			if not part.get('ranges'):
				if part.get("data"):

					uuid = part['data']['clientId']
					p_t = ""
					for poss in question['answers']:
						if poss['identifier'] == uuid:
							#print(poss)
							p_t = poss['content']
							break
					
					part_text += f"<mark>{p_t}</mark>"
					continue
			part = part['ranges']
			
			for pod_part in part:
				if pod_part.get("text"):
					part_text += pod_part['text']
		
		output += "✔ " + part_text + "<br>"
	
	return output


async def get_checkbox_answer(question):
	output = ""

	for option in question['answers']:
		if str(option['correct']) == "True":
			output += "✔ " + option['content'] + "<br>"

	return output

async def get_correct_data(data):
	task = {}

	task['question'] = data['content']
	task['answer'] = ""

	for question in data['questions']:
		type = question['type']

		if type == "radio":
			task['answer'] += await get_radio_answer(question)

		elif type == "links":
			task['answer'] += await get_links_answer(question)

		elif type == "text":
			task['answer'] += await get_text_answer(question)

		elif type == "text_gap":
			task['answer'] += await get_text_gap_answer(question)

		elif type == "checkbox":
			task['answer'] += await get_checkbox_answer(question)
	return task

async def get_results(tasks, id, headers):
	output = []

	for task in tasks:
		url = f"https://foxford.ru/api/trainings/{id}/tasks/{task}"
		async with aiohttp.ClientSession() as session:
			async with session.get(url, headers=(headers)) as data:
				output.append(await get_correct_data(await data.json()))

	return output

async def beautify_answers(tasks):
	for task in tasks:
		print(f"Вопрос: {task['question']}\n")
		print(f"Ответ: {task['answer']}\n\n\n")

async def get_answers(url):
	t_id = url.split("trainings/")[1]
	if "/" in t_id:
		t_id = t_id.split("/")[0]
	headers = await gen_headers(t_id)

	test_data = await get_test(t_id, headers)

	if not test_data:
		print("Ошибка...")
		exit()

	print(f"Успешно получен тест: {test_data['name']}")
	
	tasks = await get_tasks_ids(data=test_data['tasks'])
	
	submits = await submit_answers(tasks, headers, t_id)
	if submits:
		await finish_test(t_id, headers)
		
		answers = await get_results(tasks, t_id, headers)
		print(await beautify_answers(answers))

asyncio.get_event_loop().run_until_complete(get_answers(test_urs[0]))