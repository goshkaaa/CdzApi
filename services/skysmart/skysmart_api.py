import json

import aiohttp
from fake_useragent import UserAgent
from CdzApi.models import SkySmartModel

from ..exceptions import *


class SkySmartApi:
	__user_agent: UserAgent = UserAgent()

	_uuids_url: str = "https://api-edu.skysmart.ru/api/v1/task/preview"
	_auth_url: str = 'https://api-edu.skysmart.ru/api/v1/auth/registration/student'
	_step_html_url: str = "https://api-edu.skysmart.ru/api/v1/content/step/load?stepUuid="	

	__auth_data: dict = {
		"userAgent": {
			"ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
			"browser": {
			"name": "Chrome",
			"version": "100.0.4896.127",
			"major": "100"
			},
			"engine": {
			"name": "Blink",
			"version": "100.0.4896.127"
			},
			"os": {
			"name": "Windows",
			"version": "10"
			},
			"device": {},
			"cpu": {
			"architecture": "amd64"
			}
		}
	}

	def __init__(self, task_hash: str):
		self.__task_hash: str = task_hash

	@staticmethod
	def _decode_unicode_escape(string: str) -> str:
		return string.encode('utf_8').decode('unicode-escape')

	async def _auth(self, session: aiohttp.ClientSession) -> str:
		headers: dict = {
			'User-Agent' : self.__user_agent.chrome,
		}
		async with session.post(url=self._auth_url, headers=headers, data=json.dumps(self.__auth_data)) as task_response:
			if task_response.status == 200:
				return 'Bearer ' + str(json.loads(await task_response.text())["jwtToken"])
			else:
				raise AuthException(await task_response.text())

	async def _get_uuids(self, session: aiohttp.ClientSession, headers: dict) -> str:
		payload: str = "{\"taskHash\":\"" + self.__task_hash + "\"}"

		async with session.post(url=self._uuids_url, data=payload, headers=headers) as task_response:
			hash_raw: dict = json.loads(await task_response.text())
			meta_info: dict = hash_raw.get("meta")

			if meta_info:
				return meta_info["stepUuids"]
			else:
				raise UnknownTestException(hash_raw)

	async def _get_step_html(self, session: aiohttp.ClientSession, headers: dict, uuid: str) -> str:
		url: str = self._step_html_url + uuid

		async with session.get(url=url, headers=headers) as task_response:
			return self._decode_unicode_escape(await task_response.text())

	async def get_htmls(self, session: aiohttp.ClientSession): #добавить тип!
		headers = {
			'User-Agent' : self.__user_agent.chrome,
			'Authorization' : await self._auth(session)
		}
		uuids: list = await self._get_uuids(session, headers)
		content_raw = await SkySmartModel.filter(uuid__in=uuids).values()

		return content_raw
			 
		

