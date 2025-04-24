from typing import Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class ExampleMiddleware(BaseMiddleware):
	outer: bool = False  # Used for automatic middleware connection. Inner if false, otherwise outer.

	def __init__(self) -> None:
		pass

	async def __call__(
		self,
		handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
		event: Message,
		data: dict[str, Any]
	) -> Any:
		pass
		return await handler(event, data)
