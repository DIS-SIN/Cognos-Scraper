"""Pre-process the extract from Cognos for integration into cloud DB."""
import logging
import os
import pandas as pd
from config import shared_directories
from config.shared_mappings import city_map
from registrations_scraper.config import directories

# Instantiate logger
logger = logging.getLogger(__name__)

### IMPORT RAW DATA ###
# Files exported by Cognos have .xls extension but are tab-separated and
# encoded with UTF-16 Little Endian
# 'object' datatype in Pandas is synonymous with 'str'
os.chdir(shared_directories.DOWNLOADS_DIR)
regs = pd.read_csv('LSR Mini.xls', sep='\t', index_col=False, encoding='utf_16_le',
				   keep_default_na=False)
if not regs.shape[0] > 0:
	logger.critical('Failure: LSR Mini.xls is empty.')
	exit()

logger.debug('1/4: Data imported.')

# Ensure column 'course_code' is uppercase
regs['course_code'] = regs['course_code'].astype(str).str.upper()

# Limit entries in column 'learner_classif' to 80 characters
# A very small number of learners put a lengthy description instead of their classification
regs['learner_classif'] = regs['learner_classif'].astype(str).str.slice(0, 80)

logger.debug('2/4: Data cleaned.')

# Create new columns 'offering_city_fr' and 'learner_city_fr' as certain cities require translation e.g. 'NCR'
regs['offering_city_fr'] = regs['offering_city_en'].map(city_map)
regs['learner_city_fr'] = regs['learner_city_en'].map(city_map)

logger.debug('3/4: New columns created.')

# Export results as CSV
os.chdir(directories.PROCESSED_DIR)
regs.to_csv('lsr_processed.csv', sep=',', encoding='utf-8', index=False,
			quotechar='"', line_terminator='\r\n')

logger.debug('4/4: Data exported.')