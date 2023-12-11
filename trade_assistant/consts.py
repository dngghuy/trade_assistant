import pathlib
import os
import pytz
from datetime import datetime, timedelta, date


class CoinTable:
    COIN_INFO = 'organization_info'
    COIN_5M_INFO = 'trading_5m'
    COIN_1H_INFO = 'trading_1h'
    COIN_4H_INFO = 'trading_4h'


class StockTable:
    STOCK_INFO = 'stock_organization_info'
    STOCK_EOD_INFO = 'stock_trading_eod'
    STOCK_5M_INFO = 'stock_trading_5m'


class TimeZone:
    GMT7_HOCHIMINH = 'Asia/Ho_Chi_Minh'


SRC_FOLDER = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
CONFIG_FOLDER = SRC_FOLDER / 'configs'
DATA_FOLDER = SRC_FOLDER / 'data'

# Postgres config file
POSTGRESQL_CONFIG_FILE = CONFIG_FOLDER / 'postgresql.yml'


# import tzlocal
#
#
# lc_time = datetime.now()
# print(tzlocal.get_localzone())
# # lc_tz = pytz.timezone(tzlocal.get_localzone())
# gmt5 = lc_time.astimezone(pytz.timezone('Etc/GMT-5'))
# gmt7 = lc_time.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))
# print(lc_time, gmt7, (gmt7 + timedelta(1)).weekday())
# import holidays
# print(holidays.country_holidays('VN'))
# print(date(2023, 9, 2) in holidays.country_holidays('VN'))
# print(lc_time.timestamp())