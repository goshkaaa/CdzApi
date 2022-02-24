import json

import aiohttp

from onlinetests.exceptions import *


class SkySmartApi:
	__login: str = "marslovandrej4@gmail.com"
	__password: str = "32qLw,wbBPDQ4Rc"

	def __init__(self, task_hash: str):
		self.task_hash: str = task_hash

	@staticmethod
	def decode_unicode_escape(string: str) -> str:
		return string.encode('utf_8').decode('unicode-escape')

	async def auth(self, session: aiohttp.ClientSession, ) -> str:
		url: str = 'https://api-edu.skysmart.ru/api/v2/auth/auth/student'
		request_data: dict = {
			"phoneOrEmail": self.__login,
			"password": self.__password
		}
		async with session.post(url=url, data=json.dumps(request_data)) as task_response:
			if task_response.status == 200:
				return 'Bearer ' + str(json.loads(await task_response.text())["jwtToken"])
			else:
				raise AuthException(await task_response.text())

	async def get_uuids(self, session: aiohttp.ClientSession, auth_token: str) -> str:
		url: str = "https://api-edu.skysmart.ru/api/v1/task/preview"
		payload = "{\"taskHash\":\"" + self.task_hash + "\"}"
		headers = {
			'Content-Type': 'application/json',
			'Authorization': auth_token
		}
		async with session.post(url=url, data=payload, headers=headers) as task_response:
			hash_raw = json.loads(await task_response.text())
			meta_info = hash_raw.get("meta")
			if meta_info:
				return meta_info["stepUuids"]
			else:
				raise UnknownTestException(hash_raw)

	async def get_step_html(self, session: aiohttp.ClientSession, auth_token: str, uuid: str) -> str:
		url = "https://api-edu.skysmart.ru/api/v1/content/step/load?stepUuid=" + uuid
		headers = {'Authorization': auth_token}
		async with session.get(
				url=url,
				headers=headers,
		) as task_response:
			return self.decode_unicode_escape(await task_response.text())
