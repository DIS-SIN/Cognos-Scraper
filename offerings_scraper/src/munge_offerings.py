"""Convert file format for mysql-connector-python."""
import logging
import os
import pandas as pd
from offerings_scraper.config import directories
from config import shared_directories

# Instantiate logger
logger = logging.getLogger(__name__)

### IMPORT RAW DATA ###
# Files exported by Cognos have .xls extension but are tab-separated and
# encoded with UTF-16 Little Endian
# 'object' datatype in Pandas is synonymous with 'str'
os.chdir(shared_directories.DOWNLOADS_DIR)
df = pd.read_csv('Offerings.xls', sep='\t', index_col=False, encoding='utf_16_le',
				 keep_default_na=False)
if not df.shape[0] > 0:
	logger.critical('Failure: Offerings.xls is empty.')
	exit()

logger.debug('1/2: Data imported.')

# Export results as CSV
os.chdir(directories.PROCESSED_DIR)
df.to_csv('offerings_processed.csv', sep=',', encoding='utf-8', index=False,
		  quotechar='"', line_terminator='\r\n')

logger.debug('2/2: Data exported.')
