import logging
import logging.config
import os
from config.logger_config import logger_dict


def main():
	# Comments scraper
	from comments_scraper.src import download_files
	from comments_scraper.src import compare_row_counts
	from comments_scraper.src import munge_comments
	from comments_scraper.src import get_sentiment
	from comments_scraper.src import push_to_db
	
	# Registrations scraper
	from registrations_scraper.src import download_files
	from registrations_scraper.src import compare_row_counts
	from registrations_scraper.src import geocode_registrations
	from registrations_scraper.src import push_to_db


def check_for_pickles():
	"""Check if pickles required for memoization are present."""
	check_sentiment_dict = os.path.isfile('./comments_scraper/pickles/sentiment_dict.pickle')
	check_geo_dict = os.path.isfile('./registrations_scraper/pickles/geo_dict.pickle')
	if not check_sentiment_dict or not check_geo_dict:
		return False
	return True


def check_for_processed_dirs():
	"""Check if dirs into which outputs will be saved are present."""
	check_comments_processed = os.path.isdir('./comments_scraper/processed')
	check_registrations_processed = os.path.isdir('./registrations_scraper/processed')
	if not check_comments_processed or not check_registrations_processed:
		return False
	return True


if __name__ == '__main__':
	# Instantiate parent logger
	logging.config.dictConfig(logger_dict)
	logger = logging.getLogger(__name__)
	
	# Check for pickles are processed dirs
	pickles = check_for_pickles()
	if not pickles:
		logger.critical('Failure: Missing pickles.')
		exit()
	dirs = check_for_processed_dirs()
	if not dirs:
		logger.critical('Failure: Missing processed directories.')
		exit()
	
	# Run app
	try:
		main()
	except Exception:
		logger.critical('Failure!', exc_info=True)
	else:
		# Assign critical level so will be seen by SlackHandler
		logger.critical('Good morning nerds. ETL ran successfully!')
