import logging
import time
from argparse import ArgumentParser
from datetime import datetime, timedelta
import pytz
import holidays

from trade_assistant.stock_crawlers.index_crawler import TCBSStockInfoGetter
from trade_assistant.database.db import PostGresLocalDatabase
from trade_assistant.stock_crawlers.stock_lists import STOCK_LISTS
from trade_assistant.utils.logging import setup_logging
from trade_assistant.consts import (
    StockTable,
    POSTGRESQL_CONFIG_FILE,
    TimeZone
)


logger = logging.getLogger()

coin_db_dict = {
    '5m': StockTable.STOCK_5M_INFO,
    'eod': StockTable.STOCK_EOD_INFO,
}


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("--type", required=True, type=str, choices=['5m', 'eod'])
    return parser.parse_args()


def main(
    interval: str,
):
    # Get the current time and convert to GMT + 7
    local_time = datetime.now()
    # vn_holidays = holidays.VN()
    gmt7_tz = local_time.astimezone(pytz.timezone(TimeZone.GMT7_HOCHIMINH))
    # Check if the time is before 9:15AM or after 2L45PM, pass
    if (gmt7_tz.hour < 9 and gmt7_tz.minute <= 15) or (gmt7_tz.hour > 14 and gmt7_tz.minute > 45):
        return
    # Check if the date is not weekdays, pass
    if gmt7_tz.weekday() > 4:
        return
    # Check if the date is not holiday, pass
    if gmt7_tz.date() in holidays.country_holidays('VN'):
        return

    local_db = PostGresLocalDatabase(
        db_config_path=POSTGRESQL_CONFIG_FILE,
        table_name=coin_db_dict.get(interval)
    )
    crawler = TCBSStockInfoGetter()
    # Currently handle a limited number of pairs, so we will do it iteratively
    # Get all tickers
    crawled_data = crawler.get_multiple_ticker_historical_data(
        symbols=STOCK_LISTS,
        start_dates=gmt7_tz.date().strftime('%Y-%m-%d'),
        end_dates=gmt7_tz.date().strftime('%Y-%m-%d')

    )
    for i in crawled_data:
        i_data = i['data']
        i_ticker = i['ticker']
        for j in i_data:
            input_dictionary = {
                "open": j["open"],
                "high": j["high"],
                "low": j["low"],
                "close": j["close"],
                "volume": j["volume"],
                "trading_date": j['tradingDate'],
                "created_at": int(gmt7_tz.timestamp()),
                "ticker": i_ticker
            }
            local_db.insert(incoming_data_item=input_dictionary)


if __name__ == '__main__':
    setup_logging()
    args_ = parse_arguments()
    main(interval=args_.type)