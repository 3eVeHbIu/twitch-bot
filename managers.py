from config import CHANNEL
from json import loads
import asyncio
import aiohttp
from time import time


managers_list = {}
viewers = {}
start_time = 0


def write_data_into_list(data):
    managers_list.clear()
    data = loads(data.decode())
    for role in data['chatters']:
        for item in data['chatters'][role]:
            if role in ['moderators', 'staff', 'admins', 'global_mods']:
                managers_list[item] = role

            if item in viewers:
                viewers[item][1] += time() - start_time
            else:
                viewers[item] = [role, 0]


async def get_json(session, url):
    async with session.get(url) as response:
        assert response.status == 200
        data = await response.read()
        write_data_into_list(data)


async def fill_manager_list():
    global start_time
    start_time = time()
    session = aiohttp.ClientSession()
    while True:
        try:
            url = 'http://tmi.twitch.tv/group/user/{}/chatters'.format(CHANNEL)
            res = await get_json(session, url)
        except AssertionError as err:
            print('Bad request status')
        except Exception as err:
            print('Faild with error:', str(err))
            break
        start_time = time()
        await asyncio.sleep(5)


def is_manager(user):
    return user in managers_list

# For debag
if __name__ == "__main__":
    async def p():
        while True:
            print(viewers)
            await asyncio.sleep(5)

    async def main():
        await asyncio.gather(p(), fill_manager_list())

    asyncio.run(main())
