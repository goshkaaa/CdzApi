import asyncpg
from tortoise import Tortoise
from models.skysmart_model import SkySmartModel
import time

async def init_db():
	await Tortoise.init(
		db_url = "postgres://cdzapidev:NotAnotherCdzApiAdmin@188.120.251.86:5432/cdzapimaindb",
		modules = {
			"models": ["models.skysmart_model", "models.resh_model"]
		}
	)

async def test_select():
	t1 = time.perf_counter()
	data = await SkySmartModel.filter(uuid="e9ab0cdc-1015-49a5-93c2-b6ef30e55e69").first().values()

	print(data)
	print("\n\n")
	print(
		round(
			time.perf_counter() - t1,
			2
		)
	)