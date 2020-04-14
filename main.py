import sock_func
import config
import threading
import socket
import re


def main():
    soc = socket.socket()
    soc.connect((config.HOST, config.PORT))
    soc.send('PASS {}\r\n'.format(config.PASSWORD).encode('utf-8'))
    soc.send('NICK {}\r\n'.format(config.NICK).encode('utf-8'))
    soc.send('JOIN #{}\r\n'.format(config.CHANNEL).encode('utf-8'))

    filling_op_list = threading.Thread(target=sock_func.fill_op_list,
                                       name='Thread2')
    filling_op_list.start()

    chat_message = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')

    print('___Bot connected___')

    while True:
        response = soc.recv(1024).decode('utf-8')
        if response == 'PING :{}\r\n'.format(config.MESSAGE_INTERFACE):
            soc.send('PONG :{}\r\n'.format(
                config.MESSAGE_INTERFACE).encode('utf-8'))
        else:
            username = re.search(r'\w+', response).group(0)
            message = chat_message.sub('', response)
            print(username + ': ' + message)
            if username in config.oplist:
                pass


if __name__ == '__main__':
    main()
