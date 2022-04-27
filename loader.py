import asyncpg
from tortoise import Tortoise
import os

async def init_db():
	tortoise_username = os.environ.get("tortoise_username")
	tortoise_password = os.environ.get("tortoise_password")
	tortoise_ip = os.environ.get("tortoise_ip")
	tortoise_port = os.environ.get("tortoise_port")
	tortoise_dbname = os.environ.get("tortoise_dbname")

	await Tortoise.init(
		db_url = "postgres://{}:{}@{}:{}/{}"\
			.format(
				tortoise_username,
				tortoise_password,
				tortoise_ip,
				tortoise_port,
				tortoise_dbname
			),
		modules = {
			"models": ["CdzApi.models.skysmart_model", "CdzApi.models.resh_model"]
		}
	)