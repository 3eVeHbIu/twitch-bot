from time import sleep
import config
from urllib.request import urlopen
from json import loads



def fill_op_list():
    while True:
        try:
            url = 'http://tmi.twitch.tv/group/user/{}/chatters'.format(
                config.CHANNEL)
            res = urlopen(url).read().decode()
            if res.find('502 bad getway') == -1:
                config.oplist.clear()
                data = loads(res)
                for item in data['chatters']['moderators']:
                    config.oplist[item] = 'moderator'
                for item in data['chatters']['staff']:
                    config.oplist[item] = 'staff'
                for item in data['chatters']['admins']:
                    config.oplist[item] = 'admin'
                for item in data['chatters']['global_mods']:
                    config.oplist[item] = 'global_mod'
            else:
                print('ERROR 502: bad getway')
        except Exception as err:
            print('Faild with error:', str(err))
            break
        print(config.oplist)
        sleep(5)


def is_op(user):
    return user in config.oplist
