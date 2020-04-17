# files
import config
from managers import fill_manager_list, is_manager
# libraries
import asyncio
import re


CHAT_MESSAGE = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')
DEPARTURE_TEMPLATE = 'PRIVMSG #{} :{}\r\n'


async def check_chat_messages():
    reader, writer = await asyncio.open_connection(config.HOST, config.PORT)
    writer.write('PASS {}\r\n'.format(config.PASSWORD).encode())
    await writer.drain()
    writer.write('NICK {}\r\n'.format(config.NICK).encode())
    await writer.drain()
    writer.write('JOIN #{}\r\n'.format(config.CHANNEL).encode())
    await writer.drain()
    print('__Connected__')

    while True:
        response = await reader.read(4096)
        response = response.decode()
        if response == 'PING :{}\r\n'.format(config.MESSAGE_INTERFACE):
            writer.write('PONG :{}\r\n'.format(
                config.MESSAGE_INTERFACE).encode())
            await writer.drain()
        else:
            username = re.search(r'\w+', response).group(0)
            message = CHAT_MESSAGE.sub('', response)[:-1]
            if is_manager(username):
                print(username + ': ' + message)


async def async_distribution():
    tasks = []
    tasks.append(asyncio.create_task(fill_manager_list()))
    tasks.append(asyncio.create_task(check_chat_messages()))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(async_distribution())
