from fastapi import FastAPI
from app.api.api_router import router
from trade_assistant.database.db_pool import DataBasePool
from trade_assistant.utils.utils import read_yml_config
from trade_assistant.consts import POSTGRESQL_CONFIG_FILE


def get_application() -> FastAPI:
    # Also starts many services here
    # Tele Bot start

    application = FastAPI()
    application.include_router(router=router, prefix='/api')

    return application


# also start postgrest for conn
app = get_application()


@app.on_event("startup")
async def startup():
    """Initialize the application server."""
    # Create a database connection pool
    await DataBasePool.setup(cfg=read_yml_config(POSTGRESQL_CONFIG_FILE))


@app.on_event("shutdown")
async def shutdown():
    # close the database connection pool on shutdown
    await DataBasePool.teardown()
