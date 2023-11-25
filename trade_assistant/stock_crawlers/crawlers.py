"""
Get the news from telegram bot
"""
from trade_assistant.stock_crawlers.index_crawler import TCBSStockInfoGetter
from trade_assistant.stock_crawlers.stock_lists import STOCK_LISTS
from typing import List
from argparse import ArgumentParser, Namespace


def arg_parse() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('--start_date', type=str, required=True)
    parser.add_argument('--end_date', type=str, required=True)
    parser.add_argument('--stocks', type=str, required=False, nargs='+', default=STOCK_LISTS)
    args = parser.parse_args()
    return args


def write_db(df: pd.DataFrame):
    pass


def main(start_date: str, end_date: str, stocks: List[str] = STOCK_LISTS):
    """
    :param start_date:
    :param end_date:
    :param stocks:
    :return:
    """
    list_results = TCBSStockInfoGetter.get_multiple_ticker_historical_data(
        symbols=stocks,
        start_dates=start_date,
        end_dates=end_date
    )

    # post process

