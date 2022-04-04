import peewee
import psycopg2

db = peewee.PostgresqlDatabase(
	database = "cdzapimaindb", 
	user = "cdzapidev", 
	password = "NotAnotherCdzApiAdmin", 
	host = "188.120.251.86", 
	port = "5432"
)

class BaseModel(peewee.Model):
	class Meta:
		database = db

class SkySmartModel(BaseModel):
	uuid = peewee.CharField(null=False)
	content = peewee.TextField(null=True)
	#не понял, что за primary key, точнее зачем он тут нужен?
	class Meta:
		db_table = 'SkySmart'
