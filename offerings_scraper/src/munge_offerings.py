"""Pre-process the extract from Cognos for integration into cloud DB."""
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

logger.debug('1/3: Data imported.')

# Remove whitespace from columns known to contain junk spacing
df['instructor_names'] = df['instructor_names'].astype(str).str.strip()
df['fiscal_year'] = df['fiscal_year'].astype(str).str.strip()
df['client'] = df['client'].astype(str).str.strip()
df['offering_language'] = df['offering_language'].astype(str).str.strip()

# Merge obscure values with standard values for 'offering_language'
df['offering_language'] = df['offering_language'].astype(str).str.replace('Simultaneous Translation', 'Bilingual').replace('ESL', 'English').replace('FSL', 'French')

logger.debug('2/3: Data cleaned.')

# Export results as CSV
os.chdir(directories.PROCESSED_DIR)
df.to_csv('offerings_processed.csv', sep=',', encoding='utf-8', index=False,
		  quotechar='"', line_terminator='\r\n')

logger.debug('3/3: Data exported.')
