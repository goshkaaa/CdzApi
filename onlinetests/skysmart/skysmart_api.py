import json
import aiohttp

class SkySmartApi:
	__login = "nettstrex@gmail.com"
	__password = "zrXwjtXa96"
	
	def __init__(self, task_hash: str):
		self.task_hash = task_hash

	def decode_unicode_escape(self, string: str) -> str:
		return string.encode('utf_8').decode('unicode-escape')

	async def auth(self) -> str:
		url = 'https://api-edu.skysmart.ru/api/v2/auth/auth/student'
		request_data = {
			"phoneOrEmail" : self.__login,
			"password" : self.__password
		}
		async with aiohttp.ClientSession() as session:
			async with session.post(
				url = url,
				data = json.dumps(request_data),   
			) as task_responce:
				if task_responce.status == 200:
					return 'Bearer '+ str(json.loads(await task_responce.text())["jwtToken"])
				else:
					raise Exception("Ошибка авторизации!") #!!!!

	async def get_room_hash(self, auth_token: str) -> str:
		url = "https://api-edu.skysmart.ru/api/v1/task/start"
		payload = "{\"taskHash\":\"" + self.task_hash + "\"}"
		headers = {
			'Content-Type': 'application/json',
			'Authorization': auth_token
		}
		async with aiohttp.ClientSession() as session:
			async with session.post(
				url = url,
				data = payload,   
				headers = headers
			) as task_responce:
				hash_raw = json.loads(await task_responce.text())
				room_hash = hash_raw.get("roomHash")
				if room_hash:
					return room_hash
				else:
					raise Exception("Не верный task_hash!") #!!!!

	async def get_uuids(self, auth_token: str) -> list:
		url = "https://api-edu.skysmart.ru/api/v1/lesson/join"
		payload = "{\"roomHash\":\"" + await self.get_room_hash(auth_token) + "\"}"
		headers = {
			'Content-Type': 'application/json',
			'Authorization': auth_token
		}
		async with aiohttp.ClientSession() as session:
			async with session.post(
				url = url,
				data = payload,   
				headers = headers
			) as task_responce:
				steps_raw = json.loads(self.decode_unicode_escape(await task_responce.text()), strict=False)
				return steps_raw['taskMeta']['stepUuids']

	async def get_step_html(self, auth_token: str, uuid: str) -> str:
		url = "https://api-edu.skysmart.ru/api/v1/content/step/load?stepUuid=" + uuid
		headers = {'Authorization': auth_token}
		async with aiohttp.ClientSession() as session:
			async with session.get(
				url = url,
				headers = headers, 
			) as task_responce:
				return self.decode_unicode_escape(await task_responce.text())

	async def get_tasks_htmls(self) -> list:
		htmls = []
		auth_token = await self.auth()
		for uuid in await self.get_uuids(auth_token):
			htmls.append(await self.get_step_html(auth_token, uuid))
		return htmls