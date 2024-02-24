from fastapi import FastAPI
from app.api.api_router import router
from trade_assistant.database.db_pool import DataBasePool
from app.settings import get_settings


def get_application() -> FastAPI:
    # Also starts many services here
    # Tele Bot start

    application = FastAPI()
    application.include_router(router=router, prefix='/api')

    return application


# also start postgrest for conn
app = get_application()
settings = get_settings()


@app.on_event("startup")
async def startup():
    """Initialize the application server."""
    # Create a database connection pool
    await DataBasePool.setup(settings=settings)


@app.on_event("shutdown")
async def shutdown():
    # close the database connection pool on shutdown
    await DataBasePool.teardown()
