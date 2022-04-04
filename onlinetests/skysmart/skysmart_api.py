import json

import aiohttp
from fake_useragent import UserAgent
from onlinetests.exceptions import *
from models.skysmart_model import SkySmartModel

# ...............…………………………._¸„„„„_
# …………………….…………...„--~*'¯…….'\
# ………….…………………… („-~~--„¸_….,/ì'Ì
# …….…………………….¸„-^"¯ : : : : :¸-¯"¯/'
# ……………………¸„„-^"¯ : : : : : : : '\¸„„,-"
# **¯¯¯'^^~-„„„----~^*'"¯ : : : : : : : : : :¸-"
# .:.:.:.:.„-^" : : : : : : : : : : : : : : : : :„-"
# :.:.:.:.:.:.:.:.:.:.: : : : : : : : : : ¸„-^¯
# .::.:.:.:.:.:.:.:. : : : : : : : ¸„„-^¯
# :.' : : '\ : : : : : : : ;¸„„-~"
# :.:.:: :"-„""***/*'ì¸'¯
# :.': : : : :"-„ : : :"\
# .:.:.: : : : :" : : : : \,
# :.: : : : : : : : : : : : 'Ì
# : : : : : : :, : : : : : :/
# "-„_::::_„-*__„„~"


class SkySmartApi:
	__user_agent: UserAgent = UserAgent()
	__login: str = "marslovandrej4@gmail.com"
	__password: str = "32qLw,wbBPDQ4Rc"

	def __init__(self, task_hash: str):
		self.__task_hash: str = task_hash

	@staticmethod
	def __decode_unicode_escape(string: str) -> str:
		return string.encode('utf_8').decode('unicode-escape')

	async def __auth(self, session: aiohttp.ClientSession) -> str:
		url: str = 'https://api-edu.skysmart.ru/api/v2/auth/auth/student'
		request_data: dict = {
			"phoneOrEmail": self.__login,
			"password": self.__password
		}
		headers: dict = {
			'User-Agent' : self.__user_agent.chrome
		}
		async with session.post(url=url, headers=headers, data=json.dumps(request_data)) as task_response:
			if task_response.status == 200:
				return 'Bearer ' + str(json.loads(await task_response.text())["jwtToken"])
			else:
				raise AuthException(await task_response.text())

	async def __get_uuids(self, session: aiohttp.ClientSession, headers: dict) -> str:
		url: str = "https://api-edu.skysmart.ru/api/v1/task/preview"
		payload: str = "{\"taskHash\":\"" + self.__task_hash + "\"}"

		async with session.post(url=url, data=payload, headers=headers) as task_response:
			hash_raw: dict = json.loads(await task_response.text())
			meta_info: dict = hash_raw.get("meta")

			if meta_info:
				return meta_info["stepUuids"]
			else:
				raise UnknownTestException(hash_raw)

	async def __get_step_html(self, session: aiohttp.ClientSession, headers: dict, uuid: str) -> str:
		url: str = "https://api-edu.skysmart.ru/api/v1/content/step/load?stepUuid=" + uuid

		async with session.get(url=url, headers=headers) as task_response:
			return self.__decode_unicode_escape(await task_response.text())

	async def get_htmls(self, session: aiohttp.ClientSession): #добавить тип!
		headers = {
			'User-Agent' : self.__user_agent.chrome,
			'Authorization' : await self.__auth(session)
		}
		uuids: list = await self.__get_uuids(session, headers)
		content_raw = await SkySmartModel.filter(uuid__in=uuids).values()
		
		return content_raw
			 
		

