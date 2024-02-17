import uvicorn
import os

from fastapi import FastAPI
from utils.utils import read_yml_config
from bot.consts import TELEGRAM_BOT_CONFIG_FILE
from app.consts import CONFIG_FILE
from app.api.api_router import router


def get_application() -> FastAPI:
    # Also starts many services here
    # Tele Bot start

    application = FastAPI()
    application.include_router(router=router, prefix='/api')

    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run(app)
