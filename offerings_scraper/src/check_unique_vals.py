"""Check for unknown values in key fields. Unexpected changes can occasionally
appear due to poor communication with DBAs.
"""
import logging
import os
import pandas as pd
from config import shared_directories
from utils.utils import _check_column
from offerings_scraper.config import unique_vals

# Instantiate logger
logger = logging.getLogger(__name__)

### IMPORT RAW DATA ###
os.chdir(shared_directories.DOWNLOADS_DIR)
df = pd.read_csv('Offerings.xls', sep='\t', index_col=False, encoding='utf_16_le',
				 keep_default_na=False)
if not df.shape[0] > 0:
	logger.critical('Failure: Offerings.xls is empty.')
	exit()
logger.debug('1/8: Data imported.')

# Check column 'business_type'
_check_column(logger, df['business_type'].unique(), unique_vals.BUSINESS_TYPE)
logger.debug('2/8: Column \'business_type\' verified.')

# Check column 'quarter'
_check_column(logger, df['quarter'].unique(), unique_vals.QUARTER)
logger.debug('3/8: Column \'quarter\' verified.')

# Check column 'offering_status'
_check_column(logger, df['offering_status'].unique(), unique_vals.OFFERING_STATUS)
logger.debug('4/8: Column \'offering_status\' verified.')

# Check column 'offering_region_en'
_check_column(logger, df['offering_region_en'].unique(), unique_vals.OFFERING_REGION_EN)
logger.debug('5/8: Column \'offering_region_en\' verified.')

# Check column 'offering_region_fr'
_check_column(logger, df['offering_region_fr'].unique(), unique_vals.OFFERING_REGION_FR)
logger.debug('6/8: Column \'offering_region_fr\' verified.')

# Check column 'offering_province_en'
_check_column(logger, df['offering_province_en'].unique(), unique_vals.OFFERING_PROVINCE_EN)
logger.debug('7/8: Column \'offering_province_en\' verified.')

logger.debug('8/8: Check complete: No unknown values.')
