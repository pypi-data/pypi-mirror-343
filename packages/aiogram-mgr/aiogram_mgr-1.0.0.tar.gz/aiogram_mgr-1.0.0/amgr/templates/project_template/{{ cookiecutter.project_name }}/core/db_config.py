def tortoise_config(db_url: str, models: list[str]):
	# EXAMPLE TORTOISE CONFIG.
	# See https://tortoise.github.io/setup.html#tortoise.Tortoise.init
	return {
		"connections": {"default": db_url},
		"apps": {
			"models": {
				"models": [*models, "aerich.models"],
				"default_connection": "default",
			},
		},
	}
