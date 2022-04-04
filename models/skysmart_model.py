from tortoise import fields
from tortoise.models import Model

class SkySmartModel(Model):
	id = fields.IntField(pk=True)
	uuid = fields.CharField(max_length=40)
	content = fields.TextField()

	def __str__(self):
		return self.uuid

	class Meta:
		table = "SkySmart"
