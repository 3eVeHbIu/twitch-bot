import asyncio
from json import loads
from random import randint
from time import monotonic

import aiohttp

from TimeClass import Time
from config import CHANNEL, BOT_LIST

managers_list = {}
viewers = {}
start_time = 0


def write_data_into_lists(data):
    managers_list.clear()
    data = loads(data.decode())
    for role in data['chatters']:
        for item in data['chatters'][role]:
            if role in ['moderators', 'staff', 'admins', 'global_mods', 'broadcaster']:
                managers_list[item] = role
            if item in viewers:
                viewers[item]['time'] += monotonic() - start_time
            else:
                viewers[item] = {'role': role, 'time': Time()}


async def get_json(session, url):
    async with session.get(url) as response:
        assert response.status == 200
        data = await response.read()
        write_data_into_lists(data)


async def fill_manager_list():
    global start_time
    start_time = monotonic()
    session = aiohttp.ClientSession()
    while True:
        try:
            url = 'http://tmi.twitch.tv/group/user/{}/chatters'.format(CHANNEL)
            await get_json(session, url)
        except AssertionError as err:
            print('Bad request status')
        except Exception as err:
            print('Failed with error:', str(err))
            break
        start_time = monotonic()
        await asyncio.sleep(randint(1, 5))


def is_manager(user):
    return user in managers_list or user in BOT_LIST
