import asyncio

import logging

from aiogram import Bot, Dispatcher
from rich.progress import Progress

from tortoise import Tortoise

from . import config, db_config
from ..apps import get_apps
from ..utils import util_dict


logger = logging.getLogger()


async def init_db(models: list[str]):
	logger.info("Initializing database...")
	await Tortoise.init(
		db_config.tortoise_config(
			db_url=config.settings.DB_URL,
			models=models
		)
	)


async def start_project():
	apps_info = get_apps()

	bot = Bot(
		token=config.settings.BOT_TOKEN,
		parse_mode=config.parse_mode
	)

	dp = Dispatcher(
		storage=config.fsm_storage,
		**util_dict  # Dependency injection
	)
	with Progress(expand=True, ) as progress:
		task = progress.add_task("Including routers...", total=len(apps_info[0]["routers"]))
		for router in apps_info[0]["routers"]:
			dp.include_router(router)
			progress.update(task, advance=1)

	logger.info("Starting bot")
	await asyncio.gather(
		dp.start_polling(bot),
		init_db(apps_info[0]["models"])
	)
	logger.info("Bot started successfully!")

