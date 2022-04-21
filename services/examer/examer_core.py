import asyncio
from http import cookies
import aiohttp
from bs4 import BeautifulSoup
import json

async def auth():
    # captcha go fuck yourself :)

    return {
        "rmbme": "QXBwQnVuZGxlXEVudGl0eVxVc2VyOmNHRnVkR2hsY2pZeE16WTNOQT09OjE2ODA5MDEzOTE6NGVkNjBlZGIxNTdkZTRiYzM4MjM2NjI3ZDYzYjg0MmEyNzM2MDE4ZjE2ODcxZjUyNmQ5MWIwMjJhNjE4NGVmMg%3D%3D"
    }

async def get_task_ids(cook, test_hash):
    url = f"https://teacher.examer.ru/api/v2/teacher/test/student/{test_hash}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, cookies=cook) as response:
            if not response.status == 200:
                # сделать raise на ошибку получения idшников !
                return None

            raw_json = await response.json()

            return await get_ids_from_json(raw_json)

async def get_ids_from_json(raw_json):
    return [id['id'] for id in raw_json["test"]["tasks"]]

async def get_test_hash(url):
    # не окончательное решение! нужны проверки!
    return url.split("/")[-1]

async def create_test(cook, task_ids):
    url     = "https://teacher.examer.ru/api/v2/teacher/test/save"
    payload = await gen_test_payload(task_ids)

    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, data=payload, cookies=cook) as response:
            print( await response.text() )
            # нихуя не ворк!(

async def gen_test_payload(task_ids):
    payload = {
        "scenario": 2,
        "id": 8,
        "name": "Орфоэпические нормы",
        "tasks": [{"id": id, "difficult": "easy"} for id in task_ids],
        "subject_id": 13,
        "alias": "rus",
        "params": {
            "showAnswers": True,
            "showProfile": True
        }
    }
    print(payload)

    return json.dumps(payload, indent=4)

async def main(url):
    test_hash     = await get_test_hash(url=url)
    cook          = await auth()
    task_ids      = await get_task_ids(cook=cook, test_hash=test_hash)
    new_test_hash = await create_test(cook=cook, task_ids=task_ids)


url = "https://t.examer.ru/a5aca"
asyncio.get_event_loop().run_until_complete(main(url))