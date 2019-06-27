import os

logger_dict = {
	'version': 1,
	'formatters': {
		'formatter': {
			'format': '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
			'datefmt': '%Y-%m-%d %H:%M:%S'
		}
	},
	'handlers': {
		'fileHandler': {
			'class': 'logging.FileHandler',
			'level': 'INFO',
			'formatter': 'formatter',
			'encoding': 'utf-8',
			'filename': 'logs/scraper.log'
		},
		'stdOutHandler': {
			'class': 'logging.StreamHandler',
			'level': 'INFO',
			'formatter': 'formatter',
			'stream': 'ext://sys.stdout'
		}
	},
	'loggers': {
		# Root logger identified with empty string
		'': {
			'handlers': ['fileHandler', 'stdOutHandler'],
			'level': 'NOTSET'
		}
	}
}
