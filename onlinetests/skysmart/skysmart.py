import bs4
from base64 import b64decode
from skysmart_api import SkySmartApi

class SkySmartAnswer:
	result = {}
	def __init__(self, task_hash: str):
		self.api = SkySmartApi(task_hash)

	def decode_base64(self, string) -> str:
		return b64decode(string).decode('utf8')

	async def get_answers(self) -> dict:
		for task_html in await self.api.get_tasks_htmls():
			pass