"""Push processed extract to cloud DB."""
import logging
from offerings_scraper.config.directories import PROCESSED_DIR
from utils.db import get_db, run_mysql

# Instantiate logger
logger = logging.getLogger(__name__)

# Store DB connection in global var to avoid reconnecting after each query
cnx = get_db()
logger.debug('1/7: Connected to DB.')

# MySQL requires paths with forward slashes
PROCESSED_DIR = PROCESSED_DIR.replace('\\', '/')

create_table = """
	CREATE TABLE new_offerings(
		offering_id INT,
		course_title_en VARCHAR(200),
		course_title_fr VARCHAR(300),
		course_code VARCHAR(20),
		business_type VARCHAR(30),
		start_date DATE,
		end_date DATE,
		offering_status VARCHAR(30),
		offering_province_en VARCHAR(30),
		offering_province_fr VARCHAR(30),
		offering_city VARCHAR(50)
	);
"""

load_data = """
	LOAD DATA LOCAL INFILE '{0}/offerings_processed.csv'
	INTO TABLE new_offerings
	FIELDS OPTIONALLY ENCLOSED BY '"'
	TERMINATED BY ','
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
	(offering_id, course_title_en, course_title_fr, course_code, business_type, @temp_start_date,
	@temp_end_date, offering_status, offering_province_en, offering_province_fr, offering_city)
	SET start_date = STR_TO_DATE(@temp_start_date, '%Y-%m-%d %T'),
	end_date = STR_TO_DATE(@temp_end_date, '%Y-%m-%d %T');
""".format(PROCESSED_DIR)

indices = []

# Rename tables in a single atomic transaction
# Ensures clean switchover + no downtime
rename_tables = """
	RENAME TABLE offerings TO old_offerings, new_offerings TO offerings;
"""

drop_table = """
	DROP TABLE old_offerings;
"""

try:
	run_mysql(cnx, create_table)
	logger.debug('2/7: New table created.')
	run_mysql(cnx, load_data)
	logger.debug('3/7: Data loaded.')
	for index in indices:
		run_mysql(cnx, index)
	logger.debug('4/7: Indices created.')
	run_mysql(cnx, rename_tables)
	logger.debug('5/7: Tables renamed.')
	run_mysql(cnx, drop_table)
	logger.debug('6/7: Old table dropped.')
except Exception as e:
	logger.critical('Failure!', exc_info=True)
	cnx.close()
	exit()
finally:
	cnx.close()
	logger.debug('7/7: Connection closed.')
