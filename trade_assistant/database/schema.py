"""
WRITING TABLE SCHEMAS HERE
"""

ORG_INFO_SCHEMA = {
    "organ_code": "TEXT",
    "ticker": "TEXT PRIMARY KEY",
    "com_group_code": "TEXT",
    "icb_code": "TEXT",
    "organ_type_code": "TEXT",
    "organ_name": "TEXT",
    "organ_short_name": "TEXT"
}

# STOCK PRICE SCHEMA
TICKER_PRICE_SCHEMA_EOD_POSTGRESQL = {
    "open": "REAL",
    "high": "REAL",
    "low": "REAL",
    "close": "REAL",
    "volume": "REAL",
    "trading_date": "TEXT",
    "created_at": "BIGINT",
    "ticker": "TEXT"
}


TICKER_PRICE_SCHEMA_5M_POSTGRESQL = {
    "open": "REAL",
    "high": "REAL",
    "low": "REAL",
    "close": "REAL",
    "volume": "REAL",
    "trading_date": "TEXT",
    "created_at": "BIGINT",
    "ticker": "TEXT"
}

# COIN PRICE SCHEMA
COIN_PRICE_SCHEMA_4H_POSTGRESQL = {
    "open_time": "BIGINT",
    "open": "FLOAT",
    "high": "FLOAT",
    "low": "FLOAT",
    "close": "FLOAT",
    "volume": "FLOAT",
    "close_time": "BIGINT",
    "quote_asset_volume": "FLOAT",
    "number_of_trades": "INTEGER",
    "taker_buy_base_asset_volume": "FLOAT",
    "taker_buy_quote_asset_volume": "FLOAT",
    "ignored": "INTEGER",
    "trading_date": "TEXT",
    "trading_pair": "TEXT"
}

COIN_PRICE_SCHEMA_5M_POSTGRESQL = {
    "open_time": "BIGINT",
    "open": "FLOAT",
    "high": "FLOAT",
    "low": "FLOAT",
    "close": "FLOAT",
    "volume": "FLOAT",
    "close_time": "BIGINT",
    "quote_asset_volume": "FLOAT",
    "number_of_trades": "INTEGER",
    "taker_buy_base_asset_volume": "FLOAT",
    "taker_buy_quote_asset_volume": "FLOAT",
    "ignored": "INTEGER",
    "trading_date": "TEXT",
    "trading_pair": "TEXT"
}

COIN_PRICE_SCHEMA_1H_POSTGRESQL = {
    "open_time": "BIGINT",
    "open": "FLOAT",
    "high": "FLOAT",
    "low": "FLOAT",
    "close": "FLOAT",
    "volume": "FLOAT",
    "close_time": "BIGINT",
    "quote_asset_volume": "FLOAT",
    "number_of_trades": "INTEGER",
    "taker_buy_base_asset_volume": "FLOAT",
    "taker_buy_quote_asset_volume": "FLOAT",
    "ignored": "INTEGER",
    "trading_date": "TEXT",
    "trading_pair": "TEXT"
}