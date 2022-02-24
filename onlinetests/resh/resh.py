import asyncio
import json

import aiohttp
from bs4 import BeautifulSoup


async def html_trans(ids,soup,uuid,x):
    a = ''
    try:
        block = soup.find('div',attrs={'class':'js-test-item test-content test-meta','data-test-id':f'{uuid}'})
        titile = (block.find('div',attrs={'class':'test__title'}).text).replace('\n','') 
    except:
        block = soup.find('div',attrs={'class':'test-meta js-test-item','data-test-id':f'{uuid}'})
        titile = (block.find('div',attrs={'class':'test__title'}).text).replace('\n','') 
    try:
        a = a + f"№{x}📝Вопрос: {titile}\n\n"
    except:
        pass
    for i in block.find_all('div', attrs={'class':'interaction-item associated-sets'}):
        for id in ids[f'{list(ids.keys())[0]}']:
            id = id['value']
            id = id.split(' ')
            a = block.find('div', attrs={'data-id':f'{id[0]}'}).text.replace('\n','') 
            b = block.find('div', attrs={'data-id':f'{id[1]}'}).text.replace('\n','') 
            a = a + f'{a} - {b}\n'

    for i in block.find_all('div', attrs={'class':'test-words'}):
        for l in i.find_all('select', attrs={'class':'interaction-item'}):
            l2 = l['data-interaction-identifier']
            for id in ids[f"{l2}"]:
                id = id['value']
                a = a + f"{(l.find('option',attrs={'data-id':f'{id}'}).text)}\n"

    for i in block.find_all('div', attrs={'class':'test-sentence interaction-item'}):        
        for id in ids[f'{list(ids.keys())[0]}']:
            id = id['value']
            id = id.split(' ')
            a = a + f"{block.find('span', attrs={'data-id':f'{id[0]}'}).text + f'- {id[1]}'}\n"
            

            
    for i in block.find_all('div', attrs={'class':'interaction-choices choices-set sort__row sort__lower-container _sortable-words _sortable-words--source'}):
        for id in ids[f'{list(ids.keys())[0]}']:
            id = id['value']
            id = id.split(' ')    
            a = a + f"{(i.find('div',attrs={'class':'interaction-choice sort__item','data-id':f'{id[1]}'}).text)}\n"

    for i in block.find_all('div', attrs={'class':'text-with-gaps test-sentence--underline'}):
        for id in ids[f'{list(ids.keys())[0]}']:
            id = id['value']
            id = id.split(' ')[0]
            for g in i.find_all('span', attrs={'data-id':f'{id}'}):
                a = a + f'{g.text}\n'
    for i in block.find_all('tr'):
        for id in ids[f'{list(ids.keys())[0]}']:
            id = id['value']
            for l in i.find_all('input', attrs={'value':f'{id}'}):
                try:
                    c = i.text.replace('\n','')
                    a = a + f"{c}\n"
                except:
                    pass
                try:
                    print(f'https://resh.edu.ru/{(i.find("img")["src"])}')
                except:
                    pass
    for i in block.find_all('div',{'class':'interaction-item tests-checkboxes'}):        
        for id in ids[f'{list(ids.keys())[0]}']:
            id = id['value']
            for l in block.find_all('input', attrs={'value':f'{id}'}):
                for n in block.find_all('label', attrs={'for':f'{l["id"]}'}):
                    try:
                        c = n.text.replace('\n','')
                        a = a + f"{c}\n"
                    except:
                        pass
                    try:
                        print(f'https://resh.edu.ru/{(n.find("img")["src"])}')
                    except:
                        pass    
    names = []
    name2 = []
    tables = block.find('table', attrs={'class':'table sort_box-border gap-match-table__table'})
    if tables is not None:
        for c in tables.find_all('td',attrs={'class':'js-interaction-choice-container'}):  
            x = c['data-identifier']
            name2.append(x)
        for l in tables.find_all('th'):
            x = l.text.replace('\n','')
            names.append(x)
        for i in range(len(names)): #names[i],name2[i]
            a = a + f"{names[i]}\n"
            for id in ids[f'{list(ids.keys())[0]}']:
                id = id['value']
                id = id.split()
                if name2[i] == id[0]:
                    taskname = soup.find('div',attrs={'data-id':f'{id[1]}'}).text
                    a = a + f'{taskname}\n'
    print(a)


async def get_answer(uuid,soup):
    x = 0
    for id in uuid:
        x = x + 1
        url = f"https://resh.edu.ru/tests/{id}/get-answers"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
            "Accept": "*/*",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                data = await resp.read()
                try:
                    hashrate = json.loads(data)
                    await session.close()
                    await html_trans(hashrate,soup,id,x)
                except:
                    pass

#https://resh.edu.ru/subject/lesson/2954/control/1/#176616

async def get_tasks(url):
    urllogin = "https://resh.edu.ru/login_check"

    payload2={'_username': 'юзернейм',
    '_password': 'пароль'}

    headers2 = {
    'Cookie': 'PHPSESSID=vg33h5d0tsa4l0i47a2vpjkocj'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
        }
    async with aiohttp.ClientSession() as session:
        async with session.post(urllogin, headers=headers2, data=payload2) as resp2:
            async with session.get(url,headers=headers) as resp:
                data = await resp.read()
                soup = BeautifulSoup(data.decode('utf-8'), 'html.parser')
                uuid = []
                for i in soup.find_all('div', attrs= {"class": "js-test-item test-content test-meta"}):
                    try:
                        uuid.append(i['data-test-id'])
                    except:
                        pass
                for i in soup.find_all('li', attrs= {"class": "test__task-num"}):
                    uuid.append(i['data-test-id'])
                await session.close()
                print(await get_answer(uuid,soup))



c = input('Введите ссылку: ')
asyncio.get_event_loop().run_until_complete(get_tasks(c))