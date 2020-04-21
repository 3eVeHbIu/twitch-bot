# files
import config
from managers import fill_manager_list, is_manager, viewers
# libraries
import asyncio
import re


CHAT_MESSAGE = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')
DEPARTURE_TEMPLATE = 'PRIVMSG #{} :{}\r\n'


def make_time_req(item):
    time = int(item[1][1])
    if item[1][1] < 60:
        return item[0] + ' -- ' + str(time) + ' сек'
    elif item[1][1] < 3600:
        return item[0] + ' -- ' \
            + str(time // 60) + ' мин ' \
            + str(time % 60) + ' сек'
    else:
        return item[0] + ' -- ' \
            + str(time // 3600) + ' ч ' \
            + str(time % 3600 // 60) + ' мин ' \
            + str(time % 60) + ' сек'


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
                if message.startswith('hah'):
                    request = list(viewers.items())
                    request.sort(key=lambda i: i[1][1])
                    if len(request) > 5:
                        request = request[:5]
                    request = '\n'.join([make_time_req(i) for i in request])
                writer.write(DEPARTURE_TEMPLATE.format(
                    config.CHANNEL, request).encode())


async def async_distribution():
    tasks = []
    tasks.append(asyncio.create_task(fill_manager_list()))
    tasks.append(asyncio.create_task(check_chat_messages()))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(async_distribution())
