import os
import importlib.util

from aiogram import BaseMiddleware


def get_apps():
	results = {
		"routers": [],
		"model_paths": []
	}
	app_count: int = 0

	current_directory = os.getcwd()

	for item in os.listdir(current_directory):
		item_path = os.path.join(current_directory, item)

		# check if it is an app
		if os.path.isdir(item_path) and os.path.isfile(os.path.join(item_path, '__init__.py')):
			module_name = f"{item}"
			module_path = os.path.join(item_path, '__init__.py')

			spec = importlib.util.spec_from_file_location(module_name, module_path)
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)

			if hasattr(module, 'router'):
				results["routers"].append(module.router)
				app_count += 1

			if hasattr(module, 'models'):
				results["model_paths"].append(f"apps.{module_name}.models")

	return results, app_count


routers: list[str] = []  # Put routers here if you disabled auto_router_search in the config.
models: list[str] = []  # Put model file paths here if you disabled auto_model_search in the config.
middlewares: list[BaseMiddleware] = []  # Put your middlewares here if you disabled auto_middleware_search in the config
