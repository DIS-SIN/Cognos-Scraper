import json
import logging
import os
import requests
import time

assert os.environ.get('SLACK_BOT_URL', None) is not None, 'Missing environ var SLACK_BOT_URL.'

class SlackHandler(logging.Handler):
	"""Custom handler to store log record in JSON and send in POST request."""
	def emit(self, record):
		"""Set headers and URL."""
		log_entry = self.format(record)
		url = os.environ.get('SLACK_BOT_URL')
		return requests.post(url, log_entry, headers={'Content-type': 'application/json'}).content


class SlackFormatter(logging.Formatter):
	"""Custom formatter to structure JSON object as required by Slack."""
	def __init__(self):
		super(SlackFormatter, self).__init__()
	
	def format(self, record):
		"""Unpack record object and assemble into string."""
		asc_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(record.created)))
		level_name = record.levelname
		name = record.name
		message = record.msg
		return_string = f'{asc_time} - {level_name} - {name} - {message}'
		data = {'text': return_string}
		return json.dumps(data)


# Add custom handler to logging library
logging.handlers.SlackHandler = SlackHandler

logger_dict = {
	'version': 1,
	'formatters': {
		'formatter': {
			'format': '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
			'datefmt': '%Y-%m-%d %H:%M:%S'
		},
		'slackFormatter': {
			'()': SlackFormatter
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
		},
		'slackHandler': {
			'class': 'logging.handlers.SlackHandler',
			'level': 'CRITICAL',
			'formatter': 'slackFormatter'
		}
	},
	'loggers': {
		# Root logger identified with empty string
		'': {
			'handlers': ['fileHandler', 'stdOutHandler', 'slackHandler'],
			'level': 'NOTSET'
		}
	}
}
