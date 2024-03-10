import psycopg2
from contextlib import closing
import pandas as pd
from trade_assistant.consts import (
    CoinTable,
    POSTGRESQL_CONFIG_FILE,
)
from trade_assistant.database.db import PostGresLocalDatabase


coin_db_dict = {
    '5m': CoinTable.COIN_5M_INFO,
    '4h': CoinTable.COIN_4H_INFO,
}


class StrategyBacktester:
    def __init__(
            self,
            start_date: str,
            end_date: str,
            list_symbols: list,
            list_intervals: list
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.list_symbols = list_symbols
        self.list_intervals = list_intervals
        self.environment = None
        self._load_env()

    def _load_env(self):
        """

        :return:
        """
        env_dict = {}
        for interval in self.list_intervals:
            local_db = PostGresLocalDatabase(
                db_config_path=POSTGRESQL_CONFIG_FILE,
                table_name=coin_db_dict.get(interval)
            )
            list_dfs = []
            for symbol in self.list_symbols:
                query = f"""
                    SELECT * 
                    FROM {coin_db_dict.get(interval)} 
                    WHERE trading_pair = '{symbol}'
                    AND trading_date BETWEEN '{self.start_date}' AND '{self.end_date}' 
                    ORDER BY close_time desc 
                    """
                df = pd.read_sql_query(query, local_db.conn)
                list_dfs.append(df)
            total_df = pd.concat(list_dfs, axis=0)
            env_dict[interval] = total_df
        self.environment = env_dict

    def backtest(self):
        pass