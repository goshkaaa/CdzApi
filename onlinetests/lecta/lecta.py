from onlinetests.lecta.lecta_api import LectaApi
from onlinetests.skysmart.skysmart import SkySmartAnswer

class LectaAnswer(SkySmartAnswer):

	def __init__(self, task_hash):
		self.api = LectaApi(task_hash)		