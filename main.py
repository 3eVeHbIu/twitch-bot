# files
import chat_comands
import config
# libraries
import asyncio
import threading
import socket
import re


CHAT_MESSAGE = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')


async def check_chat_messages():
    reader, writer = await asyncio.open_connection(config.HOST, config.PORT)
    writer.write('PASS {}\r\n'.format(config.PASSWORD).encode())
    writer.write('NICK {}\r\n'.format(config.NICK).encode())
    writer.write('JOIN #{}\r\n'.format(config.CHANNEL).encode())
    await writer.drain()
    while True:
        response = await reader.read(1024)
        response = response.decode()
        if response == 'PING :{}\r\n'.format(config.MESSAGE_INTERFACE):
            writer.write('PONG :{}\r\n'.format(
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


async def async_distribution():
    tasks = []
    tasks.append(asyncio.create_task(check_chat_messages()))
    tasks.append(asyncio.create_task(print_time()))
    await asyncio.gather(*tasks)





    # filling_op_list = threading.Thread(target=sock_func.fill_op_list,
    #                                    name='Thread2')
    # filling_op_list.start()

if __name__ == '__main__':
    asyncio.run(async_distribution())
