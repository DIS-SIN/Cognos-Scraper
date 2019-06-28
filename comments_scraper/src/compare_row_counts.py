"""Ensure freshly downloaded file(s) has row count(s) greater than
or equal to current DB row count(s).
"""
import logging
import os
import pandas as pd
from config import shared_directories
from utils.db import get_db, query_mysql

# Instantiate logger
# logger = logging.getLogger(__name__)

# Store DB connection in global var to avoid reconnecting after each query
cnx = get_db()
print('1/5: Connected to DB.')

# Get total row count from DB
total_count = """
	SELECT COUNT(*)
	FROM comments;
"""

# Get row counts by course code from DB
# Further insurance against garbled files (known issue with Cognos)
course_code_count = """
	SELECT course_code, COUNT(survey_id)
	FROM comments
	GROUP BY course_code;
"""

try:
	total_count_db = query_mysql(cnx, total_count)
	total_count_db = total_count_db[0][0]
	course_code_count_db = query_mysql(cnx, course_code_count)
	course_code_count_db = [(tup[0].decode(), tup[1]) for tup in course_code_count_db]
	print('2/5: Queried DB for row count: {0} rows.'.format(total_count_db))
except Exception:
	# logger.critical('Failure!', exc_info=True)
	cnx.close()
	exit()
finally:
	cnx.close()
	print('3/5: Connection closed.')

# Get total row count from Pandas
os.chdir(shared_directories.DOWNLOADS_DIR)
comments = pd.read_csv('Comments.xls', sep='\t', index_col=False, encoding='utf_16_le',
                       dtype={'survey_id': 'object'}, keep_default_na=False)
total_count_pd = comments.shape[0]
print('4/5: Queried Pandas for row count: {0} rows.'.format(total_count_pd))

# Compare row counts; exit if data missing
if total_count_pd < total_count_db:
	print('Failure: Missing data in latest Cognos extract.')
	exit()

# Get row counts by course code from Pandas
course_code_count_pd = comments['course_code'].value_counts(sort=False, dropna=False)
course_code_count_pd = {tup[0]: tup[1] for tup in course_code_count_pd.iteritems()}

# Compare DB counts with Pandas counts, using DB as baseline
for tup in course_code_count_db:
	course_code = tup[0]
	db_count = tup[1]
	pd_count = course_code_count_pd.get(course_code, 0)
	if pd_count < db_count:
		print('Failure: Missing data in latest Cognos extract for course code {0}.'.format(course_code))
		exit()

print('5/5: Check complete: No missing data.')
