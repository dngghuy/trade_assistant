"""
One-time file for DB init at local.
"""
import logging
from trade_assistant.consts import POSTGRESQL_CONFIG_FILE, StockTable
from trade_assistant.stock_crawlers.stock_lists import STOCK_LISTS
from trade_assistant.database.schema import (
    ORG_INFO_SCHEMA,
    TICKER_PRICE_SCHEMA_5M_POSTGRESQL,
    TICKER_PRICE_SCHEMA_EOD_POSTGRESQL
)
from trade_assistant.utils.logging import setup_logging
from trade_assistant.database.db import PostGresLocalDatabase


logger = logging.getLogger()


def main():
    # Initialize DB
    logger.info("Initialize DB")
    local_stock_db = PostGresLocalDatabase(
        db_config_path=str(POSTGRESQL_CONFIG_FILE),
        table_name=StockTable.STOCK_5M_INFO
    )
    # Create if not exists
    local_stock_db.create(schema=TICKER_PRICE_SCHEMA_5M_POSTGRESQL, partition_note="")

    local_stock_db.conn.commit()
    local_stock_db.conn.close()
    logger.info("Done")


if __name__ == '__main__':
    setup_logging()
    main()
