
class MeshApi:
	__login = "spottlight"
	__password = "UnaHi$6cf!4H3!7"

	def __init__(self, test_type: str, test_variant: str):
		self.test_type = test_type
		self.test_variant = test_variant

	async def auth(self) -> str:
		url = "https://uchebnik.mos.ru/api/sessions"
		session_data = {
			"login": self.__login,
			"password_hash2": hashlib.md5(self.__password.encode()).hexdigest()
		}
		async with aiohttp.ClientSession() as session:
			async with session.post(
				url = url,
				data = json.dumps(session_data),
				headers = {
					"Content-type": "application/json",
					"Accept": "application/json; charset=UTF-8"}
					) as session_response:
				if session_response.status == 200:
					return json.loads(await session_response.text())
				else:
					raise Exception("Ошибка авторизации!") #!!!!

	async def get_tasks(self) -> list:
		auth_data = await self.auth()
		url = "https://uchebnik.mos.ru/exam/rest/secure/testplayer/group"
		request_data = {
			"test_type": "training_test",
			"generation_context_type": self.test_type,
			"generation_by_id": self.test_variant
		}
		request_cookies = {
			"auth_token": auth_data["authentication_token"],
			"profile_id": str(auth_data["id"]),
			"udacl": "resh"
		}
		async with aiohttp.ClientSession() as session:
			async with session.post(
				url = url,
				data = json.dumps(request_data),
				cookies = request_cookies,
				headers = {"Content-type": "application/json"}      
			) as task_responce:
				tasks = json.loads(await task_responce.text()).get("training_tasks")
				if tasks:
					return tasks
				else:
					raise Exception("Тест не существует!") #!!!!