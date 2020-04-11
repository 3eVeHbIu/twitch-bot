import config
import api
import socket
import re
#import thread
import time


def main():
    soc = socket.socket()
    soc.connect((config.HOST, config.PORT))
    soc.send('PASS {}\r\n'.format(config.PASSWORD).encode('utf-8'))
    soc.send('NICK {}\r\n'.format(config.NICK).encode('utf-8'))
    soc.send('JOIN #{}\r\n'.format(config.CHANNEL).encode('utf-8'))

    api.mess(soc, 'Всем ку в этом чатике')


if __name__ == '__main__':
    main()
