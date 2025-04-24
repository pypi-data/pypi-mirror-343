# Configuration file of the project
# It is recommended that you use .env file provided for sensitive data (tokens).
import logging

import aiogram
from rich.logging import RichHandler

from aiogram.fsm.storage.memory import MemoryStorage
from pydantic_settings import BaseSettings


# Settings should contain sensitive information and/or information that doesnt affect projects inner workings
class Settings(BaseSettings):
	BOT_TOKEN: str  # You can edit any fields as long as they exist in .env file too

	DB_URL: str  # JDBC database url

	class Config:
		case_sensitive = True
		env_file = ".env"


settings = Settings()


# Bot config
fsm_storage = MemoryStorage()  # See https://docs.aiogram.dev/en/latest/dispatcher/finite_state_machine/storages.html
parse_mode = None  # default parse mode for bots messages. See https://core.telegram.org/bots/api#formatting-options


# Project config
auto_router_search = True  # If enabled will search for routers in apps automatically. If disabled, you should specify
# Them in apps/__init__.py yourself.

auto_model_search = True  # If enabled will search for tortoise orm Models automatically. If disabled, you should
# specify them in apps/__init__.py yourself.

# logger configuration. See https://www.structlog.org/en/stable/configuration.html for more

FORMAT = "%(message)s"
logging.basicConfig(
	level="NOTSET",
	format=FORMAT,
	datefmt="[%Y.%m.%d %H.%M.%S]",
	handlers=[
		RichHandler(
			rich_tracebacks=True,
			tracebacks_suppress=[aiogram]  # Remove this if you want to see aiogram`s logs
		),
	],
)
