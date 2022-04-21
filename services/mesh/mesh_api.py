import hashlib
import json

import aiohttp

from ..exceptions import *


class MeshApi:
	__login: str = "spottlight"
	__password: str = "Eqh#0nf6"
	__headers: dict = {
		"Content-type": "application/json",
		"Accept": "application/json; charset=UTF-8"
	}

	def __init__(self, test_type: str, test_variant: str):
		self.test_type: str = test_type
		self.test_variant: str = test_variant

	async def __auth(self, session: aiohttp.ClientSession) -> dict:
		url: str = "https://uchebnik.mos.ru/api/sessions"
		session_data: dict = {
			"login": self.__login,
			"password_hash2": hashlib.md5(self.__password.encode()).hexdigest()
		}
		async with session.post(url=url, data=json.dumps(session_data), headers=self.__headers) as session_response:
			if session_response.status == 200:
				return json.loads(await session_response.text())
			else:
				raise AuthException(await session_response.text())

	async def get_tasks(self, session: aiohttp.ClientSession) -> list:
		auth_data: dict = await self.__auth(session)
		url: str = "https://uchebnik.mos.ru/exam/rest/secure/testplayer/group"
		request_data = {
			"test_type": "training_test",
			"generation_context_type": self.test_type,
			"generation_by_id": self.test_variant
		}
		request_cookies: dict = {
			"auth_token": auth_data["authentication_token"],
			"profile_id": str(auth_data["id"]),
			"udacl": "resh"
		}
		async with session.post(url=url, data=json.dumps(request_data), cookies=request_cookies, headers=self.__headers) as task_responce:
			tasks = json.loads(await task_responce.text()).get("training_tasks")
			if tasks:
				return tasks
			else:
				raise UnknownTestException(tasks)
