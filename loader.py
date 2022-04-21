import asyncpg
from tortoise import Tortoise


async def init_db():
	await Tortoise.init(
		db_url = "postgres://cdzapidev:NotAnotherCdzApiAdmin@188.120.251.86:5432/cdzapimaindb",
		modules = {
			"models": ["models.skysmart_model", "models.resh_model"]
		}
	)