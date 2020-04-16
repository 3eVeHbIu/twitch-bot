import config
from urllib.request import urlopen


def mess(sock, message):
    sock.send('PRIVMSG #{} :{}\r\n'.format(
        config.CHANNEL, message).encode('utf-8'))


def ban(sock, user):
    mess(sock, '.ban {}'.format(user))


def unban(sock, user):
    mess(sock, '.unban {}'.format(user))


def timeout(sock, user, seconds=500):
    mess(sock, '.timeout {} {}:'.format(user, seconds))


