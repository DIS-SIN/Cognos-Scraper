import logging
import os
import pandas as pd
from comments_scraper.config import directories
from comments_scraper.mappings.city_map import city_map
from config import shared_directories

# Instantiate logger
logger = logging.getLogger(__name__)

### IMPORT RAW DATA ###
# Files exported by Cognos have .xls extension but are tab-separated and
# encoded with UTF-16 Little Endian
# 'object' datatype in Pandas is synonymous with 'str'
os.chdir(shared_directories.DOWNLOADS_DIR)
comments = pd.read_csv('Comments.xls', sep='\t', index_col=False, encoding='utf_16_le',
                       dtype={'survey_id': 'object'}, keep_default_na=False)
assert comments.shape[0] > 0, 'Unable to load comments: Null report'

logger.info('1/4: Data imported.')

# Ensure column 'course_code' is uppercase
comments['course_code'] = comments['course_code'].astype(str).str.upper()

# Remove whitespace from column 'fiscal_year'
comments['fiscal_year'] = comments['fiscal_year'].astype(str).str.strip()

# Limit entries in column 'learner_classif' to 80 characters
# A very small number of learners put a lengthy description instead of their classification
comments['learner_classif'] = comments['learner_classif'].astype(str).str.slice(0, 80)

logger.info('2/4: Data cleaned.')

# Create new column 'offering_city_fr' as certain cities require translation e.g. 'NCR'
comments['offering_city_fr'] = comments['offering_city_en'].map(city_map)

### IMPORT MAPPINGS ###

# Import mapping to overwrite column 'short_question'
os.chdir(directories.MAPPINGS_DIR)
short_question_map = pd.read_csv('short_question_map.csv', sep=',',
                                 index_col=0, squeeze=True, encoding='utf-8')
assert short_question_map.shape[0] > 0, 'Unable to load short_question_map'

# Import mapping for new column 'text_answer_fr'
os.chdir(directories.MAPPINGS_DIR)
text_answer_map = pd.read_csv('text_answer_map.csv', sep=',',
                              index_col=0, squeeze=True, encoding='utf-8')
assert text_answer_map.shape[0] > 0, 'Unable to load text_answer_map'

# Import mapping for column 'overall_satisfaction'
os.chdir(shared_directories.DOWNLOADS_DIR)
overall_sat_map = pd.read_csv('Overall Satisfaction.xls', sep='\t', index_col=0,
                              squeeze=True, encoding='utf_16_le')
assert overall_sat_map.shape[0] > 0, 'Unable to load overall_sat_map'

# Create new column 'short_question'
# Stores re-mapped questions e.g. 'Issue Description' and its variants all mapped to
# 'Comment - Technical'
comments['short_question'] = comments['original_question'].map(short_question_map)

# Check if column 'short_question' properly mapped
# Unknown values would be assgined value 'np.nan', which has dtype 'float'
# Therefore, check all values have dtype 'str'
assert all([isinstance(short_question, str) for short_question in comments['short_question'].unique()]), 'Mapping short_question failed'

# Create new column 'text_answer_fr'
# Only applies to questions with pre-defined answers like 'Yes' and 'No'
# Free text entries not translated, therefore left as empty string
comments['text_answer_fr'] = comments['text_answer'].map(text_answer_map).fillna('')

# Create new column 'overall_satisfaction'
# Rarely, a learner will have left a comment without indicating overall satisfaction
# Assign these comments value '\N' (null integer in MySQL)
comments['overall_satisfaction'] = comments['survey_id'].map(overall_sat_map).fillna('\\N')

logger.info('3/4: New columns created.')

# Export results as CSV
os.chdir(directories.PROCESSED_DIR)
comments.to_csv('comments_processed.csv', sep=',', encoding='utf-8', index=False,
                quotechar='"', line_terminator='\r\n')

logger.info('4/4: Data exported.')
