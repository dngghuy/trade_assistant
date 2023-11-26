"""
Get data from TCBS Public API
"""


import pandas as pd
import requests
from multiprocessing import Pool
import time
from typing import List, Union

DATE_FORMAT = '%Y%d%m'


class TCBSStockInfoGetter:
    TCANALYSIS = 'https://apipubaws.tcbs.com.vn/tcanalysis/v1'
    STOCK_INSIGHT = 'https://apipubaws.tcbs.com.vn/stock-insight/v1'
    NUM_PROCESSES = 16

    @staticmethod
    def get_ticker_overview(symbol: str) -> pd.DataFrame:
        """
        response columns:
        ['exchange', 'shortName', 'industryID', 'industryIDv2', 'industry', 'industryEn', 'establishedYear',
        'noEmployees', 'noShareholders', 'foreignPercent', 'website', 'stockRating', 'deltaInWeek', 'deltaInMonth',
        'deltaInYear', 'outstandingShare', 'issueShare', 'companyType', 'ticker']
        """
        data = requests.get(f'{TCBSStockInfoGetter.TCANALYSIS}/ticker/{symbol}/overview').json()
        df = pd.json_normalize(data)
        return df

    @staticmethod
    def get_ticker_historical_data(symbol: str, start: str, end: str) -> dict:
        fd = int(time.mktime(time.strptime(start, "%Y-%m-%d")))
        td = int(time.mktime(time.strptime(end, "%Y-%m-%d")))
        data = requests.get(f'{TCBSStockInfoGetter.STOCK_INSIGHT}/stock/bars-long-term?ticker={symbol}&type=stock&resolution=D&from={fd}&to={td}').json()

        return data

    @staticmethod
    def get_multiple_ticker_historical_data(
            symbols: Union[List[str], str],
            start_dates: Union[List[str], str],
            end_dates: Union[List[str], str],
            multiprocess: bool = False
    ) -> List:
        if not isinstance(symbols, list) and isinstance(symbols, str):
            symbols = [symbols]
        if not isinstance(start_dates, list) and isinstance(start_dates, str):
            start_dates = [start_dates] * len(symbols)
        if not isinstance(end_dates, list) and isinstance(end_dates, str):
            end_dates = [end_dates] * len(symbols)

        results_list = []
        if not multiprocess:
            for num, symbol in enumerate(symbols):
                results = TCBSStockInfoGetter.get_ticker_historical_data(
                    symbol=symbol,
                    start=start_dates[num],
                    end=end_dates[num]
                )
                results_list.append(results)
        else:
            if len(symbols) <= 10:
                chunk_size = 1
            else:
                chunk_size = max(1, len(symbols) // 400)
            process_input = [
                (symbol, start, end)
                for (symbol, start, end) in zip(symbols, start_dates, end_dates)
            ]
            with Pool(processes=TCBSStockInfoGetter.NUM_PROCESSES) as pool:
                results = pool.starmap_async(func=TCBSStockInfoGetter.get_ticker_historical_data, iterable=process_input, chunksize=chunk_size)
                for i in results.get():
                    results_list.append(i)

        return results_list
