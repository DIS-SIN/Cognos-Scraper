"""Ensure freshly downloaded file(s) have row count(s) greater than
or equal to current DB row count(s).
"""
import logging
import pandas as pd
from config import shared_directories
from utils.db import get_db, query_mysql

# Instantiate logger
logger = logging.getLogger(__name__)

# Store DB connection in global var to avoid reconnecting after each query
cnx = get_db()
logger.info('1/5: Connected to DB.')

# Get row count of table 'comments'
count_comments = """SELECT COUNT(*)	FROM comments;"""

try:
	results = query_mysql(cnx, count_comments)
	db_row_count = results[0][0]
	logger.info('2/5: Queried DB for row count: {0} rows.'.format(db_row_count))
except Exception:
	logger.critical('Failure!', exc_info=True)
	cnx.close()
	exit()
finally:
	cnx.close()
	logger.info('3/5: Connection closed.')

# Get row count of latest 'Comments.xls' file
comments = pd.read_csv('Comments.xls', sep='\t', index_col=False, encoding='utf_16_le',
                       dtype={'survey_id': 'object'}, keep_default_na=False)
file_row_count = comments.shape[0]
logger.info('4/5: Queried Pandas for row count: {0} rows.'.format(file_row_count))

# Compare row counts; exit if data missing
if file_row_count < db_row_count:
	logger.critical('Failure: Missing data in latest Cognos extract.')
	exit()

logger.info('5/5: Check complete.')
