import asyncpg
from asyncpg import Pool
from typing import Optional
from app.settings import Settings


class UninitializedDatabasePoolError(Exception):
    def __init__(
        self,
        message="The database connection pool has not been properly initialized.Please ensure setup is called",
    ):
        self.message = message
        super().__init__(self.message)


class DataBasePool:

    _db_pool: Optional[Pool] = None

    @classmethod
    async def setup(cls, settings: Settings, timeout: Optional[float] = None):
        connection_kwargs = {
            "host": settings.POSTGRES_HOST,
            "port": settings.POSTGRES_PORT,
            "user": settings.POSTGRES_USER,
            "password": settings.POSTGRES_PASSWORD,
            "database": settings.POSTGRES_DATABASE
        }
        cls._db_pool = await asyncpg.create_pool(**connection_kwargs)
        cls._timeout = timeout

    @classmethod
    async def get_pool(cls):
        if not cls._db_pool:
            raise UninitializedDatabasePoolError()
        return cls._db_pool

    @classmethod
    async def teardown(cls):
        if not cls._db_pool:
            raise UninitializedDatabasePoolError()
        await cls._db_pool.close()