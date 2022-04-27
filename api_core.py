import json
import re
from lib2to3.pgen2.token import OP
from typing import Optional

from fastapi import FastAPI, Header, Response
from pydantic import BaseModel

from api_service import *
from api_variables import *
from CdzApi import main

import traceback

app = FastAPI()

class solve_params(BaseModel):
    auth_token: Optional[str] = None # токен авторизации
    url: Optional[str] = None # ссылка на тест


@app.on_event("startup") # запускаем все нужные системы до запуска
async def startup_event() -> None: 
    await init_redis()

@app.get("/ping")
async def ping_handler():
    return resp["ping"]

@app.post("/solve")
async def solve_any(params: solve_params, response: Response):
    if not params.auth_token: # не предоставлен токен авторизации
        response.status_code = 401
        return resp["solve"]["auth_error"]

    if not params.url: # не предоставлена ссылка на тест
        response.status_code = 400
        return resp["solve"]["url_blank"]

    if not await check_auth_token(params.auth_token): # проверка токена
        
        return resp["solve"]["invalid_params.auth_token"]

    try:
        response = await main(params.url)

        return response
    except:
        print("ERROR: {}".format(traceback.format_exc()))
        return {"message": "error"}