"""Ensure freshly downloaded file(s) has row count(s) greater than
or equal to current DB row count(s). This is to ensure corrupted files
(known issue in Cognos) aren't pushed to DB.
"""
import logging
import os
import pandas as pd
from config import shared_directories
from utils.db import get_db, query_mysql

# Instantiate logger
logger = logging.getLogger(__name__)

# Store DB connection in global var to avoid reconnecting after each query
cnx = get_db()
logger.info('1/5: Connected to DB.')

# Get row counts by course code from DB
# Don't filter by status and can be changed by learners at any time
course_code_query = """
	SELECT course_code, COUNT(reg_id)
	FROM lsr_this_year
	GROUP BY course_code;
"""

try:
	course_code_count_db = query_mysql(cnx, course_code_query)
	course_code_count_db = [(tup[0].decode(), tup[1]) for tup in course_code_count_db]
	logger.info('2/5: Queried DB for row counts.')
except Exception:
	logger.critical('Failure!', exc_info=True)
	cnx.close()
	exit()
finally:
	cnx.close()
	logger.info('3/5: Connection closed.')

# Get total row count from Pandas
os.chdir(shared_directories.DOWNLOADS_DIR)
regs = pd.read_csv('LSR Mini.xls', sep='\t', index_col=False, encoding='utf_16_le',
                   keep_default_na=False)

# Get row counts by course code from Pandas
course_code_count_pd = regs['course_code'].value_counts(sort=False, dropna=False)
course_code_count_pd = {tup[0]: tup[1] for tup in course_code_count_pd.iteritems()}
logger.info('4/5: Queried Pandas for row counts.')

# Compare DB counts with Pandas counts, using DB as baseline
for tup in course_code_count_db:
	course_code = tup[0]
	db_count = tup[1]
	pd_count = course_code_count_pd.get(course_code, 0)
	if pd_count < db_count:
		logger.critical('Failure: Missing data in latest Cognos extract for course code {0}.'.format(course_code))
		exit()

logger.info('5/5: Check complete: No missing data.')
