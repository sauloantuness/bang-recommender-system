import requests
import json
import asyncio
import aiohttp
import os.path
import pandas as pd
from pprint import pprint
from datetime import datetime
from glob import glob

def get_users_id(pos=1001, count=2000):
    url = 'https://uhunt.onlinejudge.org/api/rank/{}/{}'.format(pos, count)
    users_id = []

    for user in requests.get(url).json():
        users_id.append(user['userid'])

    return users_id


async def fetch_user_solutions(user_id):
    url = 'https://uhunt.onlinejudge.org/api/subs-user/{}'.format(user_id)

    if os.path.isfile('uva_solutions/{}.json'.format(user_id)):
        return

    response = await aiohttp.request('GET', url)
    data = await response.text()

    f = open('uva_solutions/{}.json'.format(user_id), '+w')
    f.write(data)
    f.close()



def download_users_solutions():
    futures = [fetch_user_solutions(user_id) for user_id in get_users_id()]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(futures))


def convert_date(date):
    date = datetime.fromtimestamp(int(date))
    return date.strftime('%y/%m/%d %I:%M')


def get_user_solutions(user_id):
    ACCEPTED = 90

    SOLUTION = 0
    PROBLEM = 1
    VEREDICT = 2
    DATE = 4

    f = open('uva_solutions/{}.json'.format(user_id))
    subs = json.load(f)['subs']

    subs.sort(key=lambda x: x[DATE])

    problems = []
    solutions = []

    for sub in subs:
        if sub[VEREDICT] != ACCEPTED:
            continue

        if sub[PROBLEM] in problems: 
            continue

        solutions.append({
            'user_id': user_id,
            'solution_id' : sub[SOLUTION],
            'problem_id': sub[PROBLEM],
            'date': convert_date(sub[DATE]),
        })

        problems.append(sub[PROBLEM])

    return solutions


def get_uri_category(uva_category):
    ADHOC = 2
    STRING = 3
    LIBRARIES = 4
    MATH = 5
    PARADIGMS = 6
    GRAPH = 7
    GEOMETRY = 8

    uri_categories = [
        ADHOC,
        LIBRARIES,
        PARADIGMS,
        GRAPH,
        MATH,
        STRING,
        GEOMETRY,
    ]

    return uri_categories[uva_category]


def _get_book_problems():
    url = 'https://uhunt.onlinejudge.org/api/cpbook/3'

    ADHOC = 0
    LIBRARIES = 1
    PARADIGMS = 2
    GRAPH = 3
    MATH = 4
    STRING = 5
    GEOMETRY = 6

    categories = [
        ADHOC,
        LIBRARIES,
        PARADIGMS,
        GRAPH,
        MATH,
        STRING,
        GEOMETRY
    ]

    r = requests.get(url)
    cpbook = r.json()

    cpbook_problems = []

    for category in categories:
        chapter = cpbook[category]

        for i, sub in enumerate(chapter['arr']):
            for j, subsub in enumerate(sub['arr']):
                for k, problem in enumerate(subsub[1:]):
                    cpbook_problems.append({
                        'problem_id': abs(problem),
                        'category_id': get_uri_category(category),
                        'starred': True if problem < 0 else False,
                        'chapter': '{}.{}.{}'.format(i+1, j+1, k+1),
                    })

    return cpbook_problems

def _get_all_problems():

    url = 'https://uhunt.onlinejudge.org/api/p'

    ID = 0
    NUMBER = 1
    NAME = 2
    SOLVED = 3

    problems = {}

    for problem in requests.get(url).json():
        problems[problem[NUMBER]] = {
            'name': problem[NAME],
            'solved': problem[SOLVED],
            'problem_id': problem[ID],
            'problem_number': problem[NUMBER],
        }

    return problems


def get_problems():
    book_problems = _get_book_problems()
    all_problems = _get_all_problems()

    problems = {}

    for problem in book_problems:
        problem_id = problem['problem_id']
    
        problems[problem_id] = {
            **problem,
            'solved': all_problems[problem_id]['solved'],
            'name': all_problems[problem_id]['name'],
        }

    return problems


# get_users_id()
# print(get_user_solutions(703913))
# pprint(get_problems())

# problems
# for user_id in get_users_id():

# i = 0
# for user_id in get_users_id():
#     get_user_solutions(user_id)
#     print(i)
#     i += 1



def create_uva_problems():
    problems = get_problems()
    problems = [problem for problem in problems.values()]

    df = pd.DataFrame.from_dict(problems)
    df.to_csv('problems_uva.csv', index=False)

def create_uva_solutions():
    problems = get_problems()
    problems_id = problems.keys()

    users_id = [f.split('/')[-1].split('.')[0] for f in glob('./uva_solutions/*.json')]

    solutions = []

    for user_id in users_id:
        user_solutions = get_user_solutions(user_id)

        for solution in user_solutions:
            if solution['problem_id'] not in problems_id:
                continue

            solutions.append({
                **solution,
                **problems[solution['problem_id']]
            })

        print('.', end='', flush=True)



    solutions_df = pd.DataFrame.from_dict(solutions)

    solutions_df.to_csv(
        'solutions_uva2.csv',
        index=False,
        columns=['user_id', 'problem_id', 'date', 'category_id', 'solved', 'name', 'starred']
    )


# download_users_solutions()
# create_uva_solutions()
create_uva_problems()