from .lecta_api import LectaApi
from ..skysmart.skysmart_answer import SkySmartAnswer

class LectaAnswer(SkySmartAnswer):

	def __init__(self, task_hash):
		self.api = LectaApi(task_hash)		