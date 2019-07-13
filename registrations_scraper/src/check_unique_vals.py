"""Check for unknown values in key fields. Unexpected changes can occasionally
appear due to poor communication with DBAs.
"""
import logging
import os
import pandas as pd
from config import shared_directories
from utils.utils import _check_column
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
logger.debug('1/12: Data imported.')

# Check column 'business_type'
_check_column(logger, regs['business_type'].unique(), unique_vals.BUSINESS_TYPE)
logger.debug('2/12: Column \'business_type\' verified.')

# Check column 'month_en'
_check_column(logger, regs['month_en'].unique(), unique_vals.MONTH_EN)
logger.debug('3/12: Column \'month_en\' verified.')

# Check column 'offering_status'
_check_column(logger, regs['offering_status'].unique(), unique_vals.OFFERING_STATUS)
logger.debug('4/12: Column \'offering_status\' verified.')

# Check column 'offering_language'
_check_column(logger, regs['offering_language'].unique(), unique_vals.OFFERING_LANGUAGE)
logger.debug('5/12: Column \'offering_language\' verified.')

# Check column 'offering_region_en'
_check_column(logger, regs['offering_region_en'].unique(), unique_vals.OFFERING_REGION_EN)
logger.debug('6/12: Column \'offering_region_en\' verified.')

# Check column 'offering_province_en'
_check_column(logger, regs['offering_province_en'].unique(), unique_vals.OFFERING_PROVINCE_EN)
logger.debug('7/12: Column \'offering_province_en\' verified.')

# Check column 'learner_province'
_check_column(logger, regs['learner_province'].unique(), unique_vals.LEARNER_PROVINCE)
logger.debug('8/12: Column \'learner_province\' verified.')

# Check column 'reg_status'
_check_column(logger, regs['reg_status'].unique(), unique_vals.REG_STATUS)
logger.debug('9/12: Column \'reg_status\' verified.')

# Check column 'no_show'
_check_column(logger, regs['no_show'].unique(), unique_vals.NO_SHOW)
logger.debug('10/12: Column \'no_show\' verified.')

# Check column 'learner_language'
_check_column(logger, regs['learner_language'].unique(), unique_vals.LEARNER_LANGUAGE)
logger.debug('11/12: Column \'learner_language\' verified.')

logger.debug('12/12: Check complete: No unknown values.')
