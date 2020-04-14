import config
from urllib.request import urlopen
from time import sleep
from json import loads
import threading


def mess(sock, message):
    sock.send('PRIVMSG #{} :{}\r\n'.format(
        config.CHANNEL, message).encode('utf-8'))


def ban(sock, user):
    mess(sock, '.ban {}'.format(user))


def unban(sock, user):
    mess(sock, '.unban {}'.format(user))


def timeout(sock, user, seconds=500):
    mess(sock, '.timeout {} {}:'.format(user, seconds))


def fill_op_list():
    while True:
        try:
            url = 'http://tmi.twitch.tv/group/user/{}/chatters'.format(
                config.CHANNEL)
            res = urlopen(url).read().decode()

            # Не уверен что это нужно ловить именно так.
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

        # Написать нормальные исключения!!!!!!!
        except:
            print('Failed to get json')

        print(config.oplist)
        sleep(3)


def is_op(user):
    return user in config.oplist
