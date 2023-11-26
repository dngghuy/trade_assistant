"""
One-time file for DB init at local.
"""
import logging
from trade_assistant.consts import POSTGRESQL_CONFIG_FILE, StockTable
from trade_assistant.stock_crawlers.index_crawler import TCBSStockInfoGetter
from trade_assistant.stock_crawlers.stock_lists import STOCK_LISTS
from trade_assistant.database.schema import (
    ORG_INFO_SCHEMA,
    TICKER_PRICE_SCHEMA_5M_POSTGRESQL,
    TICKER_PRICE_SCHEMA_EOD_POSTGRESQL
)
from trade_assistant.utils.logging import setup_logging
from trade_assistant.database.db import PostGresLocalDatabase
from datetime import datetime, timedelta


logger = logging.getLogger()


def main():
    # Initialize DB
    logger.info("Initialize DB")
    local_stock_db = PostGresLocalDatabase(
        db_config_path=str(POSTGRESQL_CONFIG_FILE),
        table_name=StockTable.STOCK_EOD_INFO
    )
    # Create if not exists
    crawler = TCBSStockInfoGetter()
    start_date = datetime.strptime("2018-01-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-11-24", "%Y-%m-%d")

    date_list = [start_date + timedelta(days=x) for x in range(0, (end_date - start_date).days)]

    # Currently handle a limited number of pairs, so we will do it iteratively
    # Get all tickers
    crawled_data = crawler.get_multiple_ticker_historical_data(
        symbols=STOCK_LISTS,
        start_dates=start_date.strftime('%Y-%m-%d'),
        end_dates=end_date.strftime('%Y-%m-%d')
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
                "created_at": int(datetime.now().timestamp()),
                "ticker": i_ticker
            }

            local_stock_db.insert(incoming_data_item=input_dictionary)


if __name__ == '__main__':
    setup_logging()
    main()
