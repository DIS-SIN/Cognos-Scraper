"""Check for unknown values in key fields. Unexpected changes can occasionally
appear due to poor communication with DBAs.
"""
import logging
import os
import pandas as pd
from config import shared_directories
from comments_scraper.config import unique_vals

# Instantiate logger
logger = logging.getLogger(__name__)

### IMPORT RAW DATA ###
os.chdir(shared_directories.DOWNLOADS_DIR)
comments = pd.read_csv('Comments.xls', sep='\t', index_col=False, encoding='utf_16_le',
                       dtype={'survey_id': 'object'}, keep_default_na=False)
if not comments.shape[0] > 0:
	logger.critical('Failure: Comments.xls is empty.')
	exit()

logger.info('1/4: Data imported.')

# Check column 'quarter'
quarter = comments['quarter'].unique()
for elem in quarter:
	if elem not in unique_vals.QUARTER:
		logger.critical('Failure: Unknown value \'{0}\' in latest Cognos extract.'.format(elem))
		exit()

logger.info('2/4: Column \'quarter\' verified.')

# Check column 'quarter'
original_question = comments['original_question'].unique()
for elem in original_question:
	if elem not in unique_vals.ORIGINAL_QUESTION:
		logger.critical('Failure: Unknown value \'{0}\' in latest Cognos extract.'.format(elem))
		exit()

logger.info('3/4: Column \'original_question\' verified.')

logger.info('4/4: Check complete: No unknown values.')
