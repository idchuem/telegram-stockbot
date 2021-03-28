import sys
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
sys.path.append('C:/dataproject/stock_price_analysis')
from utils.stock_parser import GetStock



class Commands(GetStock):
    MODE = 'us'
    FROM_DATE ='2019-01-01'
    TODAY = datetime.now(tz=timezone(timedelta(hours=-3))).date()
    TODAY_STR = TODAY.strftime('%Y-%m-%d')
    WEEK_AGO = TODAY + timedelta(days=-7)
    WEEK_AGO_STR = WEEK_AGO.strftime('%Y-%m-%d')
    MONTH_AGO = TODAY + timedelta(days=-30)
    MONTH_AGO_STR = MONTH_AGO.strftime('%Y-%m-%d')

    def __init__(self):
        super().__init__()
        plt.rcParams['axes.grid'] = True
        plt.ioff()
        plt.rc('font', size=9, family='NANUMBARUNGOTHIC')

    @classmethod
    def us(self, update, context):
        txt = """You can query America stock data\nPlease enter US ticker."""
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
        self.MODE = 'us'

    def kr(self, update, context):
        update.message.text = update.message.text.split()[1] if len(update.message.text.split()) > 0 else update.message.text.split()
        chat_id = update.effective_chat.id
        self.MODE = 'kr'
        msg_type = update.message.entities
        if not msg_type:
            txt = """You can query Korea stock data.\nPlease enter company name or code."""
            context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
        else:
            code = update.message.text.strip().upper()
            data = self.get_kr(code, self.FROM_DATE)
            res = self.make_text(data)
            data['MA20'] = data[code].rolling(window=20).mean()
            data['MA60'] = data[code].rolling(window=60).mean()
            data['MA120'] = data[code].rolling(window=120).mean()
            fig, ax = plt.subplots()
            ax.plot(data)
            plt.xticks(rotation=45)
            ax.legend(data.columns, fontsize=10)
            fig.savefig('photo.png', bbox_inches="tight")


            krw = '\\' if self.MODE == 'kr' else ''
            usd = '$' if self.MODE != 'kr' else ''
            send_msg = """
            {code} price from {from_date}\nrecent: {usd}{price}{krw} ({change}%)\nWeek: {usd}{w_price}{krw} ({w_change}%)\nMonth: {usd}{m_price}{krw} ({m_change}%)
            """.format(
                code=code, from_date=self.FROM_DATE, usd=usd, krw=krw,
                price=res[0], change=res[1], w_price=res[2], w_change=res[3], m_price=res[4], m_change=res[5]
            )
            context.bot.send_photo(chat_id=chat_id, photo=open('photo.png', 'rb'), caption=send_msg)


    @classmethod
    def fred(self, update, context):
        txt = """You can query FRED's data.\nPlease enter FRED ticker.\n"""
        fred_ticker = {'국채10년물': 'DGS10', '국채2년물': 'DGS2', '국채10년-2년': 'T10Y2Y', '고용율':'UNRATE', '근로자수':'PAYEMS'}
        for name, ticker in fred_ticker.items():
            txt += '{}: {}\n'.format(name, ticker)
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
        self.MODE = 'fred'

    @classmethod
    def list(self, update, context):
        txt = """You can query FRED's data.\nPlease enter FRED ticker.\n"""
        fred_ticker = {'국채10년물': 'DGS10', '국채2년물': 'DGS2', '국채10년-2년': 'T10Y2Y', '고용율':'UNRATE', '근로자수':'PAYEMS'}
        for name, ticker in fred_ticker.items():
            txt += '{}: {}\n'.format(name, ticker)
        context.bot.send_message(chat_id=update.effective_chat.id, text=txt)
        self.MODE = 'fred'

    def make_text(self, data):
        recent_day = data.iloc[-1].name
        week_ago = recent_day + relativedelta(weeks=-1)
        month_ago = recent_day + relativedelta(months=-1)
        price_recent = round(data.loc[recent_day].item(), 2)
        day_change = round(((data.loc[recent_day] - data.iloc[-2]) / data.iloc[-2] * 100).item(), 1)
        price_one_week_ago = round(data.loc[week_ago].item(), 2)
        week_change = round(((price_recent - data.loc[week_ago]) / data.loc[week_ago] * 100).item(), 1)
        price_one_month_ago = round(data.loc[month_ago].item(), 2)
        month_change = round(((price_recent - data.loc[month_ago]) / data.loc[month_ago] * 100).item(), 1)

        return price_recent, day_change, price_one_week_ago, week_change, price_one_month_ago, month_change


    def echo(self, update, context=None):
        chat_id = update.effective_chat.id
        print(context)
        print(update)
        from_date = self.FROM_DATE
        if self.MODE == 'us':
            code = update.message.text.strip().upper()
            data = self.get_us(code, from_date)
            res = self.make_text(data)
            data['MA20'] = data[code].rolling(window=20).mean()
            data['MA60'] = data[code].rolling(window=60).mean()
            data['MA120'] = data[code].rolling(window=120).mean()

            fig, ax = plt.subplots()
            ax.plot(data)
            plt.xticks(rotation=45)
            ax.legend(data.columns, fontsize=10)
            fig.savefig('photo.png', bbox_inches="tight")

        elif self.MODE == 'kr':
            code = update.message.text.strip().upper()
            data = self.get_kr(code, from_date)
            res = self.make_text(data)
            data['MA20'] = data[code].rolling(window=20).mean()
            data['MA60'] = data[code].rolling(window=60).mean()
            data['MA120'] = data[code].rolling(window=120).mean()
            fig, ax = plt.subplots()
            ax.plot(data)
            plt.xticks(rotation=45)
            ax.legend(data.columns, fontsize=10)
            fig.savefig('photo.png', bbox_inches="tight")

        elif self.MODE == 'fred':
            code = update.message.text.strip()
            data = self.get_fred(code, from_date)
            fig, ax = plt.subplots()
            ax.plot(data)
            plt.xticks(rotation=45)
            fig.savefig('photo.png', bbox_inches="tight")
            send_msg = "{code} price from {from_date}\n\n".format(code=code, from_date=from_date)
            context.bot.send_photo(chat_id=chat_id, photo=open('photo.png', 'rb'),caption=send_msg)
            return
        else:
            data = 'failed to quiry'
            context.bot.send_message(chat_id=chat_id, text=data)
            return
        krw = '\\' if self.MODE == 'kr' else ''
        usd = '$' if self.MODE != 'kr' else ''
        send_msg = """
        {code} price from {from_date}\nrecent: {usd}{price}{krw} ({change%)\nWeek: {usd}{w_price}{krw} ({w_change}%)\nMonth: {usd}{m_price}{krw} ({m_change}%)
        """.format(
            code=code, from_date=from_date, usd=usd, krw=krw,
            price=res[0], change=res[1], w_price=res[2], w_change=res[3], m_price=res[4], m_change=res[5]
        )
        context.bot.send_photo(chat_id=chat_id, photo=open('photo.png', 'rb'),caption=send_msg)

