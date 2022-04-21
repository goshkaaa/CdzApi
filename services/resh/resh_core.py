#переписать!!!
import json
from bs4 import BeautifulSoup as bs
import random
import aiohttp
import asyncio
headers = {
    "Referer": "https://resh.edu.ru/subject/lesson/2954/control/2/#176621",
    "Cookie": "_ym_uid=1633979292855242447; _ym_d=1640179753; _ym_visorc=b; _ym_isad=1; PHPSESSID=fee7q67kfrah7arkjhheaqvn99",
    "Host": "resh.edu.ru",
    "sec-ch-ua-mobile": "?0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


async def get_unsorted_answer(id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://resh.edu.ru/tests/{id}/get-answers", headers=headers) as data:
            data = await data.json()
            return data

async def get_test(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as data:
                return await data.text()
    except: return (False)

async def get_type_resh(task):
    divs = task.find_all("div")

    for div in divs:
        try:return(div["data-interaction-type"])
        except:continue

    divs = task.find_all("input")

    for div in divs:
        try:return(div["data-interaction-type"])
        except:continue

    return str(task).split('data-interaction-type="')[1].split('"')[0]

async def parse_other_task_ids(html):
    global tasks
    global parse

    tasks = []
    parse = bs(html, "html.parser")

    tasks_list = parse.find_all("div", {"class" : "scene"})

    for task in tasks_list:
        ids = task.find_all("div")
        for d in ids:
            try:id=d["data-test-id"]
            except:pass
        title = ""

        possible_titles = task.find_all("div", {"class": "test__title"})

        for titl in possible_titles:
            title = titl.find_all("p")[0].text

        task_type = await get_type_resh(task)

        tasks.append(
            {
                "id": id,
                "type": task_type,
                "title": title,
                "unsorted_answer": await get_unsorted_answer(id),
                "answer": ""
            }
        )
    return(tasks)

async def parse_task_ids(html):
    global tasks
    global parse


    tasks = []
    parse = bs(html, "html.parser")


    tasks_list = parse.find_all("div", {"class" : "markdown-test_block"})

    for task in tasks_list:

        try:id = task.find_all("div", {"class" : "js-test-item test-content test-meta"})[0]["data-test-id"]
        except:return await parse_other_task_ids(html)

        title = ""
        possible_titles = task.find_all("div", {"class" : "test__title"})

        for titl in possible_titles:
            title = titl.find_all("p")[0].text

        task_type = await get_type_resh(task)

        tasks.append(
            {
                "id" : id,
                "type" : task_type,
                "title" : title,
                "unsorted_answer" : await get_unsorted_answer(id),
                "answer" : ""
            }
        )

    return tasks


async def parse_answer(tasks):
    counter = 0

    for task in tasks:
        try:
            if task["type"] == "single_choice":
                tasks[counter]["answer"] = await get_single_choice_answer(task['unsorted_answer'], task["id"])

            elif task["type"] == "multiple_choice":
                tasks[counter]["answer"] = await get_multiple_choice_answer(task["unsorted_answer"])

            elif task["type"] == "text_entry":
                tasks[counter]["answer"] = await get_text_entry_answer(task["unsorted_answer"])

            elif task["type"] == "images_text_entries":
                tasks[counter]["answer"] = "в разработке"

            elif task["type"] == "gap_match_table":
                tasks[counter]["answer"] = await get_gap_match_table_answer(task["unsorted_answer"])

            elif task["type"] == "order":
                tasks[counter]["answer"] = await get_order_answer(task["unsorted_answer"])

            elif task["type"] == "order_vertical":
                tasks[counter]["answer"] = "в разработке"

            elif task["type"] == "two_sets_association":
                tasks[counter]["answer"] = await get_two_sets_association_answer(task["unsorted_answer"], task["id"])

            elif task["type"] == "gap_match_text":
                tasks[counter]["answer"] = await get_gap_match_text_answer(task["unsorted_answer"], task["id"])

            elif task["type"] == "gap_match_multiple_choice":
                tasks[counter]["answer"] = "в разработке"

            elif task["type"] == "inline_choice":
                tasks[counter]["answer"] = await get_inline_choice_answer(task["unsorted_answer"])

            elif task["type"] == "gap_match_color":
                tasks[counter]["answer"] = await get_gap_match_color_answer(task["unsorted_answer"], task["id"])

            elif task["type"] == "gap_match_matrix":
                tasks[counter]["answer"] = "в разработке"

            elif task["type"] == "gap_match_underline":
                tasks[counter]["answer"] = await get_gap_match_underline_answer(task["unsorted_answer"], task["id"])

            else:
                tasks[counter]["answer"] = "в разработке"
        except:
            tasks[counter]["answer"] = "не удалось получить ответ"

        counter+=1


    return tasks


async def get_gap_match_underline_answer(data, id):
    html = parse.find_all("div", {"data-test-id": id})[0]

    values = []
    answer = ""

    for response in data:
        for value in data[response]:
            values.append(value['value'].split(' ')[0])


    for value in values:
        answer += "• " + html.find_all("span", {"data-id" : value})[0].text.strip() + '<br><hr class="dropdown-divider">'

    return answer

async def get_gap_match_color_answer(data, id):
    html = parse.find_all("div", {"data-test-id" : id})[0]

    matches = {}
    answer = ""

    for response in data:
        for value in data[response]:
            matches[value['value'].split(" ")[0]] = value['value'].split(" ")[1]

    for word in matches:
        option = html.find_all("span", {"data-id" : word})[0].text.strip()
        color = html.find_all("div", {"data-id" : matches[word]})[0].text.strip()
        answer += "• " + option + " → " + color + '<br><hr class="dropdown-divider">'

    return answer

async def get_inline_choice_answer(data):
    answer = ""

    for response in data:
        for correct in data[response]:
            answer += "• " + parse.find_all("option", {"value" : correct['value']})[0].text.strip() + '<br><hr class="dropdown-divider">'

    return answer

async def get_gap_match_text_answer(data, id):
    html = parse.find_all("div", {"data-test-id" : id})[0]

    matches = {}

    for response in data:
        for option in data[response]:
            matches[option['value'].split(" ")[0]] = option['value'].split(" ")[1]

    html = html.find_all("div", {"class" : "interaction-item"})[0]

    for match in matches:
        matches[match] = html.find_all("div", {"data-id" : matches[match]})[0].text.strip()

    sorted_html = str(html.find_all("div")[0])

    for span in html.find_all("span"):
        sorted_html = sorted_html.replace(str(span), "[" + matches[span["data-id"]] + "]")

    sorted_html = sorted_html.replace("<br/>", '<br><hr class="dropdown-divider">')

    helpless = bs(sorted_html, "html.parser")
    helplesss = helpless.find_all("div")[0]["class"]
    helpless = ""
    for k in helplesss:
        helpless += k
        if helplesss.index(k)+1 != len(helplesss):
            helpless += " "

    sorted_html = sorted_html.split(f'<div class="{helpless}">')[1].split("</div>")[0]


    return sorted_html

async def get_two_sets_association_answer(data, id):
    answer = ""

    html = parse.find_all("div", {"data-test-id" : id})[0]

    for response in data:
        try:
            for match in data[response]:
                match = match['value'].split(" ")

                option1 = match[0]
                option2 = match[1]

                answer += str(html.find_all("div", {"data-id": option1})[0]).split("<p>")[1].split("</p>")[0].strip()\
                    .replace('<img src="', '<img src="https://resh.edu.ru') + " → "
                answer += str(html.find_all("div", {"data-id": option2})[0]).split("<p>")[1].split("</p>")[0].strip()\
                    .replace('<img src="','<img src="https://resh.edu.ru') + '<br><hr class="dropdown-divider">'
        except:
            answer = "не удалось получить ответ"

    return answer

async def get_order_answer(data):
    answer = ""

    for text in data:
        text_id = text
        text_div = parse.find_all("div", {"data-interaction-identifier" : text_id})[0]

        for order in data[text_id]:
            order = order["value"]
            answer += "• " + text_div.find_all("span", {"data-interaction-choice-identifier" : order})[0].text.strip() + '<br><hr class="dropdown-divider">'

    return answer

async def get_text_entry_answer(data):
    answer = ""
    for response in data:
        for positional in data[response]:
            answer += "• " + positional['value'] + '<br><hr class="dropdown-divider">'

    return answer

async def get_multiple_choice_answer(data):
    answer = ""

    for response in data:
        for option in data[response]:
            answer += "• " + str(parse.find_all("label", {"for" : parse.find_all("input", {"value" : option['value']})[0]['id']})[0])\
                .split('">')[1].split("</label>")[0].strip()\
                    .replace('<img src="', '<img src="https://resh.edu.ru').replace("<p>", "").replace("</p>", "")

            answer += '<br><hr class="dropdown-divider">'

    return answer

async def get_single_choice_answer(data, id):
    answer = parse.find_all("div", {"data-test-id" : id})

    for response in data:
        uid = data[response][0]['value']
        for item in answer:
            if item.find_all("input", {"value" : uid}) != []:
                answer = str(item.find_all("td")[-1]).split("<td>")[1].split("</td")[0].strip().replace('<img src="','<img src="https://resh.edu.ru')
    return answer

async def get_gap_match_table_answer(data):
    tables = parse.find_all("table")

    table_titles = []
    sorted_titles = []

    for response in data:
        for option in data[response]:

            title = option['value'].split(" ")[0]
            if title not in sorted_titles:
                table_titles.append({"table" : title, "title" : ""})
                sorted_titles.append(title)

    for table in tables:
        for tt in table.find_all("td", {"data-identifier" : table_titles[0]["table"]}):

            if tt != [] and len(table.find_all("td")) == len(table_titles):

                tabs = table.find_all("h4")

                tab_c = 0
                for tab in tabs:

                    table_titles[tab_c]["title"] = tab.text

                    tab_c += 1

                answer = ""

                for response in data:
                    for option in data[response]:
                        mat = option['value'].split(" ")[1]
                        unsorted_data = parse.find_all("div", {"data-id" : mat})[0]
                        answer += str(unsorted_data).split('<span class="interaction-choice__remove"></span>')[1].split("</div>")[0]\
                            .replace('src="', '<img src="https://resh.edu.ru').strip() + " → "
                        for possible_table in table_titles:
                            if possible_table["table"] == option['value'].split(" ")[0]:
                                answer += possible_table["title"] + '<br><hr class="dropdown-divider">'

                return answer

async def gen_html_resh(tasks):
    output = ""
    for task in tasks:
        output+=f"""
<div class="header_eye_search">
<div class="header_info_content">
  <div class="sub_info_tit">
    <div class="column_interest_sec">
      <div class="title_inter">Вопрос:</div><br>
    </div>
  </div>
  <div class="title">
    <h2><div class="card text-white bg-dark mb-3"><div class="card-body">{task["title"]}</div></div></h2>
  </div>
  <div class="sub_info_tit">
    <div class="column_interest_sec">
      <div class="title_inter">Ответ:</div>
      <div class="title">
        <h2><div class="card text-white bg-dark mb-3"><div class="card-body">{task["answer"]}</div></div></h2>
      </div>
    </div>
  </div>
</div>
</div>        
"""
    return output

async def get_answers_resh(url, output_type):
    idd = random.randint(1000000, 9999999)

    answers = (await parse_answer(await parse_task_ids(await get_test(url))))

    if answers != []:
        return {"var" : idd, "data" : answers}

    return False

"""
special for sinergia daddy <33
"""
async def get_ans_sinergia():
    print(
        await get_answers_resh(
            url=input("url > "),
            output_type=0 #тип вывода сделан для бота, так что 0 по умолчанию
        )
    )

loop = asyncio.get_event_loop()

loop.run_until_complete(
    get_ans_sinergia()
)