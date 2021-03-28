import telegram
from telegram.botcommand import BotCommand
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
import logging

tok = '1698241361:AAEaxCqCCAgvZh2PI2PxZlicjB2HQA7JqXs'

class TelegramBot:
    def __init__(self, name, token=tok):
        self.core = telegram.Bot(token)
        self.init_commands()
        self.updater = Updater(token)
        self.filters = Filters()
        self.id = '809524742'
        self.name = name

    def init_commands(self):
        """
        bot의 command를
        :return: None
        """
        self.core.set_my_commands([BotCommand('kr','query Korea stock price1'),
                                   BotCommand('us','query US stock price1'),
                                   BotCommand('fred','query FRED stock price1')])

    def sendMessage(self, text):
        self.core.sendMessage(chat_id=self.id, text=text)

    def add_handler(self, cmd, func):
        """
        :param cmd: Telegram 명령어 리스트 (either str, List)
        :param func: Callback 해줄 함수
        :return:
        """
        self.updater.dispatcher.add_handler(CommandHandler(cmd, func))

    def add_echo_handler(self, func):
        echo_handler = MessageHandler(Filters.text & (~Filters.command), func)
        self.updater.dispatcher.add_handler(echo_handler)

    def add_echo_handler2(self, func):
        echo_handler2 = MessageHandler(Filters.text, func)
        self.updater.dispatcher.add_handler(echo_handler2)

    def start(self):
        self.updater.start_polling()
        #   self.updater.idle()

    def stop(self):
        self.updater.start_polling()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()

"""
Updater는 프로그래머에게 frontend를 제공한다. telegram에서 메시지를 받고 dispatcher에게 전달하는 역할을 한다.
분리된 thread에서 동작하기 때문에 각 사용자들은 bot과 개별적으로 interaction이 가능하다.
updater는 polling, webhook 방식으로 시작가능하다. 
webhook은 webhookServer나 WebhookHandler class에서 활용가능하다.
"""

"""
MessageHandler는 telegram의 메세지를 다루는데 text나 media나 status updates가 있다
pass_user_data와 pass_chat_data가 

"""


"""
class bot(TelegramBot):
    def __init__(self):
        self.token = '1698241361:AAEaxCqCCAgvZh2PI2PxZlicjB2HQA7JqXs'
        TelegramBot.__init__(self, 'jun_toy_bot', self.token)
        self.updater.stop()

    def add_handler(self, cmd, func):
        self.updater.dispatcher.add_handler(CommandHandler(cmd, func))

    def add_echo_handler(self, func):
        echo_handler = MessageHandler(Filters.text & (~Filters.command), func)
        self.updater.dispatcher.add_handler(echo_handler)

    def start(self):
        self.updater.start_polling()
        #   self.updater.idle()"""

"""
def echo(update, context):
    text = "getting {}data from {}"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text)

if __name__ == '__main__':
    token = '1698241361:AAEaxCqCCAgvZh2PI2PxZlicjB2HQA7JqXs'
    #bot = telegram.Bot(token)
    bot = bot()
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    # 명령에만 반응
    #us_handler = CommandHandler('us', bot.us)
    #kr_handler = CommandHandler('kr', bot.kr)
    #fred_handler = CommandHandler('fred', bot.fred)

    #dispatcher.add_handler(us_handler)
    #dispatcher.add_handler(kr_handler)
    #dispatcher.add_handler(fred_handler)

    # 어떤 메세지가 오더라도 반응
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # 여기가 진짜 시작작
    updater.start_polling()"""



#https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot