from config import CHANNEL, managers_list
from urllib.request import urlopen
from json import loads
import asyncio
import aiohttp


async def fill_manager_list():
    while True:
        try:
            url = 'http://tmi.twitch.tv/group/user/{}/chatters'.format(CHANNEL)
            res = urlopen(url).read().decode()
            if res.find('502 bad getway') == -1:
                managers_list.clear()
                data = loads(res)
                for item in data['chatters']['moderators']:
                    managers_list[item] = 'moderator'
                for item in data['chatters']['staff']:
                    managers_list[item] = 'staff'
                for item in data['chatters']['admins']:
                    managers_list[item] = 'admin'
                for item in data['chatters']['global_mods']:
                    managers_list[item] = 'global_mod'
            else:
                print('ERROR 502: bad getway')
        except Exception as err:
            print('Faild with error:', str(err))
            break
        await asyncio.sleep(5)
        # после выхода из цикла


def is_op(user):
    return user in managers_list
