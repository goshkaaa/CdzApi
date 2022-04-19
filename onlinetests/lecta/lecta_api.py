from onlinetests.skysmart.skysmart_api import SkySmartApi

class LectaApi(SkySmartApi):
	_uuids_url: str = "https://backend-hw.lecta.ru/api/v1/task/preview"
	_step_html_url: str = "https://backend-hw.lecta.ru/api/v1/content/step/load?stepUuid="
	_auth_url: str = "https://backend-hw.lecta.ru/api/v1/auth/registration/student"

	def __init__(self, task_hash):
		super().__init__(task_hash)

	

	