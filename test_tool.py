import requests
import json
from time import perf_counter

for _ in range(5):
    t1 = perf_counter()
    data = requests.post(
        "http://127.0.0.1:8000/solve",
        json={
            "auth_token": "test",
            "url": "https://edu.skysmart.ru/student/ketezaxege"
        }
    )

    print(round(perf_counter() - t1, 2))