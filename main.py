# files
import config
from managers import fill_manager_list, is_manager, viewers
# libraries
import asyncio
import re

CHAT_MESSAGE = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')
DEPARTURE_TEMPLATE = 'PRIVMSG #{} :{}\r\n'


async def check_chat_messages():
    global request
    reader, writer = await asyncio.open_connection(config.HOST, config.PORT)
    writer.write('PASS {}\r\n'.format(config.PASSWORD).encode())
    await writer.drain()
    writer.write('NICK {}\r\n'.format(config.NICK).encode())
    await writer.drain()
    writer.write('JOIN #{}\r\n'.format(config.CHANNEL).encode())
    await writer.drain()
    print('__Connected__')
    writer.write(DEPARTURE_TEMPLATE.format(config.CHANNEL, 'Всем ку в этом чатике').encode())
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
            if is_manager(username) or username == 'sergoarefyev':
                if message.startswith('!time'):
                    print(username + ': ' + message)
                    try:
                        request = f"{username} провел чате: {viewers[username]['time']}"
                    except Exception as err:
                        print(err)
                    else:
                        writer.write(DEPARTURE_TEMPLATE.format(config.CHANNEL, request).encode())

                if message.startswith('!top'):
                    print(username + ': ' + message)
                    try:
                        top_list = list(viewers.items())
                        top_list.sort(key=lambda i: i[1]['time'], reverse=True)
                        if len(viewers) > 5:
                            top_list = top_list[:5]
                        for index, item in enumerate(top_list):
                            request = f"{index+1}) {item[0]} - {item[1]['time']}"
                            writer.write(DEPARTURE_TEMPLATE.format(config.CHANNEL, request).encode())
                    except Exception as err:
                        print(err)


async def async_distribution():
    tasks = [asyncio.create_task(fill_manager_list()), asyncio.create_task(check_chat_messages())]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(async_distribution())
