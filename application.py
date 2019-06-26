def main():
	# Comments scraper
	from comments_scraper.src import download_files
	from comments_scraper.src import munge_comments
	from comments_scraper.src import get_sentiment
	from comments_scraper.src import push_to_db
	
	# Registrations scraper
	from registrations_scraper.src import download_files
	from registrations_scraper.src import geocode_registrations
	from registrations_scraper.src import push_to_db


if __name__ == '__main__':
	import logging.config
	# Instantiate parent logger
	logging.config.fileConfig(fname='config/logging.ini')
	logger = logging.getLogger(__name__)
	try:
		main()
	except Exception:
		logger.critical('Failure!', exc_info=True)
