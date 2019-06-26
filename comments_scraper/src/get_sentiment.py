"""Get sentiment scores for comments from the Google NLP API."""
import logging
from decimal import Decimal
import os
import pickle
import time
from google.cloud import language
import pandas as pd
from comments_scraper.config import directories

# Instantiate logger
logger = logging.getLogger(__name__)

# Ignore questions that aren't free text
IGNORE_LIST = ['GCcampus Tools Used', 'OL Available', 'Prep', 'Reason to Participate', 'Technical Issues']

# Load dataset
os.chdir(directories.PROCESSED_DIR)
df = pd.read_csv('comments_processed.csv', sep=',', index_col=False,
                 encoding='utf-8', dtype={'survey_id': 'object'}, keep_default_na=False)
if not df.shape[0] > 0:
	logger.critical('Failure: comments_processed.csv is empty.')
	exit()

logger.info('1/5: Data imported.')

# Load pickle for memoization
os.chdir(directories.PICKLE_DIR)
with open('sentiment_dict.pickle', 'rb') as f:
    sentiment_dict = pickle.load(f)

logger.info('2/5: Pickle imported.')

# Instantiate client
client = language.LanguageServiceClient()

# Total number of comments processed
ctr = 0
# New comments passed to API
api_ctr = 0

def get_sentiment_score(survey_id, original_question, short_question, text_answer, overall_satisfaction):
    """Pass text to API, return its sentiment score, and memoize results."""
    global ctr
    global api_ctr
    ctr += 1
    # Print ctr every 1000 comments
    if ctr % 1_000 == 0:
        logger.info('Finished {0} comments.'.format(ctr))
    
    if short_question in IGNORE_LIST:
        result = '\\N' # i.e. NULL for MySQL
        # No need to memoize as no expensive computation performed
        return result
    
    # Use composite key of survey_id.original_question
    pkey = '{0}.{1}'.format(survey_id, original_question)
    
    # If already processed, returned memoized result to save compute
    if pkey in sentiment_dict:
        return sentiment_dict[pkey]
    
    # Otherwise, pass to API
    api_ctr += 1
    # API has limit of 500 queries / min
    if api_ctr % 500 == 0:
        logger.info('ML\'d {0} new comments.'.format(api_ctr))
        time.sleep(60)
    try:
        document = language.types.Document(content=text_answer,
                                           type=language.enums.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(document=document).document_sentiment
        # Adjust interval from [-1, 1] to [1, 5]
        # Cast to Decimal then back to int to prevent floating point rounding errors
        result = int(round(Decimal(str((sentiment.score * 2) + 3))))
    # Comments occasionally so badly written the API can't identify the language
    except Exception:
        # Default to overall_satisfaction
        result = float(overall_satisfaction)
    # Memoize and return result
    sentiment_dict[pkey] = result
    return result

api_results = df.apply(lambda x: get_sentiment_score(x['survey_id'], x['original_question'], x['short_question'], x['text_answer'], x['overall_satisfaction']),
                       axis=1,               # Apply to each row
                       raw=False,            # Pass each cell individually as not using NumPy
                       result_type='expand') # Return DataFrame rather than Series of tuples

df['stars'] = api_results

logger.info('3/5: New column created; {0} new comments ML\'d.'.format(api_ctr))

# Export sentiment_dict to pickle for future re-use
os.chdir(directories.PICKLE_DIR)
with open('sentiment_dict.pickle', 'wb') as f:
    pickle.dump(sentiment_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

logger.info('4/5: Pickle exported.')

# Export results as CSV
os.chdir(directories.PROCESSED_DIR)
df.to_csv('comments_processed_ML.csv', sep=',', encoding='utf-8', index=False,
          quotechar='"', line_terminator='\r\n')

logger.info('5/5: Data exported.')
