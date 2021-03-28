import pandas_datareader.data as web
import pandas_datareader.fred as fred
import pandas as pd
from datetime import datetime, timedelta, timezone
import re
import logging


class GetStock:
    US_DEFAULT_CODE = '^GSPC'
    KR_DEFAULT_CODE = '005930'
    FRED_DEFAULT_CODE = 'T10Y2Y'

    DATA_START_DATE = '1/1/2007'
    KR_DATA_END_DATE = datetime.now().date().strftime('%Y-%m-%d')
    US_DATA_END_DATE = datetime.now(tz=timezone(timedelta(hours=-3))).date().strftime('%Y-%m-%d')

    PLOT_START_DATE = '1/1/2015'
    KR_PLOT_END_DATE = datetime.now().date().strftime('%Y-%m-%d')
    US_PLOT_END_DATE = datetime.now(tz=timezone(timedelta(hours=-3))).date().strftime('%Y-%m-%d')
    TAG = '[STOCK]'
    TAG_KR = '[STOCK_KR]'
    TAG_US = '[STOCK_US]'
    TAG_FRED = '[STOCK_FRED]'

    def __init__(self):
        self.logger = self.init_logger()
        self.df_kr = self.read_kr_list()

    @staticmethod
    def init_logger():
        log_handler = logging.StreamHandler()
        logger = logging.getLogger(__file__)
        formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        logger.setLevel(logging.INFO)
        return logger


    def read_kr_list(self):
        try:
            df_kr = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download')[0]
            df_kr['종목코드'] = df_kr['종목코드'].astype(int).map('{:06d}'.format)
            df_kr = df_kr.iloc[:, :3]
            df_kr.to_csv('krcode_from_krx.csv')
        except:
            self.logger.error('{tag} 국내종목 읽어오기 실패해서 파일에서 읽어옵니다.. {msg}'.format(tag=self.TAG, msg=e))
            df_kr = pd.read_csv('krcode_backup.csv', index_col=0)
        self.logger.info('{tag} 국내종목 코드 읽어오기 완료'.format(tag=self.TAG, num=len(df_kr)))
        return df_kr

    def search_code_name(self, string):
        try:
            if not re.match(r'\d{6}', string):
                name = string
                code = self.df_kr[self.df_kr['회사명'] == name]['종목코드']
                code = code.to_string(index=False).strip()
            else:
                code = string
                name = self.df_kr[self.df_kr['종목코드'] == code]['회사명']
                name = name.to_string(index=False).strip()
            self.logger.info('{tag} 종목,코드 변환 완료'.format(tag=self.TAG_KR))
        except:
            self.logger.error('{tag} 종목,코드 변환 실패. {msg}'.format(tag=self.TAG_KR, msg=e))
            return None, None
        return code, name

    def get_kr(self, code=KR_DEFAULT_CODE, start=DATA_START_DATE, end=KR_DATA_END_DATE, resample='D'):
        market = ['KOSPI', 'KOSDAQ']
        if code.upper() not in market:
            code, name = self.search_code_name(code)
        else:
            name = code
        try:
            data = web.DataReader(code, data_source='naver', start=start, end=end)
            data = data.iloc[:, [3]]
            data = data.astype(int)
            if not resample == 'D':
                data = data.resample(resample, convention='end').mean()
            data.columns = [name]
            data.index.name = None
            self.logger.info('{tag} get_kr {code} 읽어오기 성공.'.format(tag=self.TAG_KR, code=code))
        except:
            self.logger.error('{tag} get_us {code} 읽어오기 실패. {msg}'.format(tag=self.TAG, code=code, msg=e))
            data = None
        return data
    
    def get_us(self, code=US_DEFAULT_CODE, start=DATA_START_DATE, end=US_DATA_END_DATE):
        try:
            data = web.DataReader(code, data_source='yahoo', start=start, end=end)
            data = data.iloc[:, [3]]
            data.columns = [code]
            data.index.name = None
            self.logger.info('{tag} get_us {code} 읽어오기 성공.'.format(tag=self.TAG_US, code=code))
        except:
            self.logger.error('{tag} get_us {code} 읽어오기 실패. {msg}'.format(tag=self.TAG_US, code=code, msg=e))
            data = None
        return data
    
    def get_fred(self, code=FRED_DEFAULT_CODE, start=DATA_START_DATE, end=US_DATA_END_DATE):
        try:
            data = web.DataReader(code, data_source='fred', start=start, end=end)
            self.logger.info('{tag} get_fred {code} 읽어오기 성공.'.format(tag=self.TAG_FRED, code=code))
            data.columns = [code]
            data.index.name = None
        except :
            self.logger.error('{tag} get_fred {code} 읽어오기 실패. {msg}'.format(tag=self.TAG_FRED, code=code, msg=e))
            return None
        return data
