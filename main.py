# files
import chat_comands
import config
# libraries
import asyncio
import threading
import socket
import re


CHAT_MESSAGE = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')




async def check_chat_messages(soc: socket):
    while True:
        response = await soc.recv(1024).decode('utf-8')
        if response == 'PING :{}\r\n'.format(config.MESSAGE_INTERFACE):
            await soc.send('PONG :{}\r\n'.format(
                config.MESSAGE_INTERFACE).encode('utf-8'))
        else:
            username = re.search(r'\w+', response).group(0)
            message = CHAT_MESSAGE.sub('', response)
            print(username + ': ' + message)



async def print_time():
    count = 0
    while True:
        print('{} seconds have passed'.format(count))
        count += 1
        await asyncio.sleep(1)






async def async_distribution(sock):
    tasks = []
    tasks.append(asyncio.create_task(check_chat_messages(sock)))
    tasks.append(asyncio.create_task(print_time()))
    await asyncio.gather(*tasks)







def main():
    soc = socket.socket()
    soc.connect((config.HOST, config.PORT))
    soc.send('PASS {}\r\n'.format(config.PASSWORD).encode('utf-8'))
    soc.send('NICK {}\r\n'.format(config.NICK).encode('utf-8'))
    soc.send('JOIN #{}\r\n'.format(config.CHANNEL).encode('utf-8'))

    # filling_op_list = threading.Thread(target=sock_func.fill_op_list,
    #                                    name='Thread2')
    # filling_op_list.start()

    print('___Bot connected___')

    asyncio.run(async_distribution(soc))


if __name__ == '__main__':
    main()
