"""Check for unknown values in key fields. Unexpected changes can occasionally
appear due to poor communication with DBAs.
"""
import logging
import os
import pandas as pd
from config import shared_directories
from registrations_scraper.config import unique_vals

# Instantiate logger
logger = logging.getLogger(__name__)

### IMPORT RAW DATA ###
os.chdir(shared_directories.DOWNLOADS_DIR)
regs = pd.read_csv('LSR Mini.xls', sep='\t', index_col=False, encoding='utf_16_le',
                   keep_default_na=False)
if not regs.shape[0] > 0:
    logger.critical('Failure: LSR Mini.xls is empty.')
    exit()
logger.info('1/12: Data imported.')


def _check_column(col_vals, target_vals):
	"""Compare a column's unique values to target set."""
	for elem in col_vals:
		if elem not in target_vals:
			logger.critical('Failure: Unknown value \'{0}\' in latest Cognos extract.'.format(elem))
			exit()

# Check column 'business_type'
_check_column(regs['business_type'].unique(), unique_vals.BUSINESS_TYPE)
logger.info('2/12: Column \'business_type\' verified.')

# Check column 'month_en'
_check_column(regs['month_en'].unique(), unique_vals.MONTH_EN)
logger.info('3/12: Column \'month_en\' verified.')

# Check column 'offering_status'
_check_column(regs['offering_status'].unique(), unique_vals.OFFERING_STATUS)
logger.info('4/12: Column \'offering_status\' verified.')

# Check column 'offering_language'
_check_column(regs['offering_language'].unique(), unique_vals.OFFERING_LANGUAGE)
logger.info('5/12: Column \'offering_language\' verified.')

# Check column 'offering_region_en'
_check_column(regs['offering_region_en'].unique(), unique_vals.OFFERING_REGION_EN)
logger.info('6/12: Column \'offering_region_en\' verified.')

# Check column 'offering_province_en'
_check_column(regs['offering_province_en'].unique(), unique_vals.OFFERING_PROVINCE_EN)
logger.info('7/12: Column \'offering_province_en\' verified.')

# Check column 'learner_province'
_check_column(regs['learner_province'].unique(), unique_vals.LEARNER_PROVINCE)
logger.info('8/12: Column \'learner_province\' verified.')

# Check column 'reg_status'
_check_column(regs['reg_status'].unique(), unique_vals.REG_STATUS)
logger.info('9/12: Column \'reg_status\' verified.')

# Check column 'no_show'
_check_column(regs['no_show'].unique(), unique_vals.NO_SHOW)
logger.info('10/12: Column \'no_show\' verified.')

# Check column 'learner_language'
_check_column(regs['learner_language'].unique(), unique_vals.LEARNER_LANGUAGE)
logger.info('11/12: Column \'learner_language\' verified.')

logger.info('12/12: Check complete: No unknown values.')
