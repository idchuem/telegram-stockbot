import sys
import time
from chatBotModel import TelegramBot
import commands

if __name__ == '__main__':
    bot = TelegramBot('jun_bot')  # Bot객체 생성, token으로 api 접속
    cmd = commands.Commands()  # 명령어 불러오기

    bot.add_handler('us', cmd.us)  # 불러온 명령어를 telegram bot의 handler에 보내주기
    bot.add_handler('kr', cmd.kr)  # 불러온 명령어를 telegram bot의 handler에 보내주기
    bot.add_handler('fred', cmd.fred)  # 불러온 명령어를 telegram bot의 handler에 보내주기
    bot.add_echo_handler(cmd.echo)  # 불러온 명령어를 telegram bot의 handler에 보내주기
    bot.add_echo_handler2(cmd.echo)  # 불러온 명령어를 telegram bot의 handler에 보내주기

    bot.start()  # telegram bot msg handling 시작

