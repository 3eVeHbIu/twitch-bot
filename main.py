import asyncio
import re
from random import randint

import config
from managers import fill_manager_list, is_manager, viewers

CHAT_MESSAGE = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')
DEPARTURE_TEMPLATE = 'PRIVMSG #{} :{}\r\n'


async def check_chat_messages():
    request = ''
    reader, writer = await asyncio.open_connection(config.HOST, config.PORT)
    writer.write('PASS {}\r\n'.format(config.PASSWORD).encode())
    await writer.drain()
    writer.write(f'NICK {config.NICK}\r\n'.encode())
    await writer.drain()
    writer.write(f'JOIN #{config.CHANNEL}\r\n'.encode())
    await writer.drain()
    print('__Connected__')
    writer.write(DEPARTURE_TEMPLATE.format(config.CHANNEL, 'Всем ку в этом чатике').encode())
    while True:
        response = await reader.read(4096)
        response = response.decode()
        if response == f'PING :{config.MESSAGE_INTERFACE}\r\n':
            writer.write(f'PONG :{config.MESSAGE_INTERFACE}\r\n'.encode())
            await writer.drain()
        else:
            username = re.search(r'\w+', response).group(0)
            message = CHAT_MESSAGE.sub('', response)[:-1]
            if message.startswith('!time'):
                print(username + ': ' + message)
                try:
                    request = f"{username} провел чате: {viewers[username]['time']}"
                except Exception as err:
                    print(err)
                else:
                    writer.write(DEPARTURE_TEMPLATE.format(config.CHANNEL, request).encode())

            elif message.startswith('!bibametr'):
                if username == 'sergoarefyev':
                    request = f'{username}, самая большая биба в этом чате'
                elif is_manager(username):
                    request = f'{username}, ваша биба {randint(15,35)} см'
                else:
                    request = f'{username}, ваша биба {randint(5,20)} см'
                writer.write(DEPARTURE_TEMPLATE.format(config.CHANNEL, request).encode())

            elif is_manager(username) or username == 'sergoarefyev':
                if message.startswith('!top'):
                    print(username + ': ' + message)
                    try:
                        top_list = list(viewers.items())
                        top_list = [user for user in top_list if not is_manager(user[0])]
                        top_list.sort(key=lambda i: i[1]['time'], reverse=True)
                        if len(viewers) > 5:
                            top_list = top_list[:5]
                        for index, item in enumerate(top_list):
                            place = f'{index+1}){item[0]}-{item[1]["time"]}'
                            request += ' ' + place
                        writer.write(DEPARTURE_TEMPLATE.format(config.CHANNEL, request).encode())
                    except Exception as err:
                        print(err)

                # elif message.startswith('!casino'):

                # elif message.startswith('!stop'):
                #     request = 'Чат, всем бб'
                #     writer.write(DEPARTURE_TEMPLATE.format(config.CHANNEL, request).encode())
                #     writer.close()
                #     await writer.wait_closed()
                #     raise SystemExit()


async def async_distribution():
    tasks = [asyncio.create_task(fill_manager_list()), asyncio.create_task(check_chat_messages())]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(async_distribution())
