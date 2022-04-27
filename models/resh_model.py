from tortoise        import fields
from tortoise.models import Model


class ReshModel(Model):
	id = fields.IntField(pk=True)
	uuid = fields.CharField(max_length=40, unique=True)
	content = fields.TextField()

	def __str__(self):
		return self.uuid

	class Meta:
		table = "Resh"