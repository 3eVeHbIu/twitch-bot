from config import CHANNEL, managers_list
from json import loads
import asyncio
import aiohttp


def write_data_into_list(data):
    managers_list.clear()
    data = loads(data.decode())
    for item in data['chatters']['moderators']:
        managers_list[item] = 'moderator'
    for item in data['chatters']['staff']:
        managers_list[item] = 'staff'
    for item in data['chatters']['admins']:
        managers_list[item] = 'admin'
    for item in data['chatters']['global_mods']:
        managers_list[item] = 'global_mod'


async def get_json(session, url):
    async with session.get(url) as response:
        assert response.status == 200
        data = await response.read()
        write_data_into_list(data)


async def fill_manager_list():
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
        await asyncio.sleep(5)


def is_manager(user):
    return user in managers_list


if __name__ == "__main__":
    async def p():
        while True:
            print(managers_list)
            await asyncio.sleep(5)

    async def main():
        await asyncio.gather(p(), fill_manager_list())

    asyncio.run(main())
