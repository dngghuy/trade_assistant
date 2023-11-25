import logging
from contextlib import closing

import psycopg2

from trade_assistant.utils.utils import read_yml_config

logger = logging.getLogger()


class PostGresLocalCoinDatabase:
    """
    Object for create, insert data, query data.
    Other tasks (drop/ delete/ update...) can be done using the main cursor.
    """
    def __init__(self, db_config_path: str, table_name: str):
        """
        Initilization
        :param db_config_path: path for connection to local db
        """
        db_config = read_yml_config(db_config_path)
        self.conn = psycopg2.connect(**db_config)
        self.table_name = table_name
        self.main_cursor = self.conn.cursor()

    def create(self, schema: dict, partition_note: str):
        """
        Create the table if not existed
        :return:
        """
        check_query = f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name='{self.table_name}'
            and table_schema='public'
        """
        # Check if table exists
        self.main_cursor.execute(check_query)
        if len(self.main_cursor.fetchall()) > 0:
            logger.info(f"Table {self.table_name} already exists")
            return
        else:
            # Process the create table logic
            list_fields = []
            for key, value in schema.items():
                list_fields.append(f"{key} {value}")
            final_fields_definition = ', '.join(list_fields)
            create_table_query = f"""
                CREATE TABLE {self.table_name}({final_fields_definition})
                {partition_note}
            """
            self.main_cursor.execute(create_table_query)
            logger.info(f"Successfully create table {self.table_name}")

    def insert(self, incoming_data_item: dict):
        """
        Update database with incoming_data_item
        incoming_data_item should be dictionary
        """
        list_keys = []
        list_values = []
        for key, value in incoming_data_item.items():
            list_keys.append(f'{key}')
            list_values.append(value)
        final_keys = ', '.join(list_keys)
        final_values = tuple(list_values)

        insert_query = f"""
            INSERT INTO {self.table_name} ({final_keys})
            VALUES ({','.join(['%s'] * len(final_values))});
        """

        with closing(self.conn.cursor()) as inserting_cursor:
            inserting_cursor.execute(insert_query, final_values)
            self.conn.commit()

    def retrieve(self, query: str):
        """
        Retrieve from db given query
        :return: list of queried items
        """
        with closing(self.conn.cursor()) as retrieve_cursor:
            retrieve_cursor.execute(query)
            results = retrieve_cursor.fetchall()
        return results