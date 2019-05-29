from decimal import Decimal
import os
import pickle
import time
from google.cloud import language
import pandas as pd
from comments_scraper.config import directories

# Ignore questions that aren't free text
IGNORE_LIST = ['GCcampus Tools Used', 'OL Available', 'Prep', 'Reason to Participate', 'Technical Issues']

# Load dataset
os.chdir(directories.PROCESSED_DIR)
df = pd.read_csv('comments_processed.csv', sep=',', index_col=False,
                 encoding='utf-8', dtype={'survey_id': 'object'}, keep_default_na=False)

print('1/5: Data imported.')

# Load pickle for memoization
os.chdir(directories.PICKLE_DIR)
with open('memo.pickle', 'rb') as f:
    memo_dict = pickle.load(f)

print('2/5: Pickle imported.')

# Instantiate client
client = language.LanguageServiceClient()

# Total number of comments processed
ctr = 0
# New comments passed to API
api_ctr = 0

def get_sentiment_score(survey_id, short_question, text_answer, overall_satisfaction):
    """Pass text to API, return its sentiment score, and memoize results."""
    global ctr
    global api_ctr
    ctr += 1
    # Print ctr every 1000 comments
    if ctr % 1_000 == 0:
        print('Finished {0} comments!'.format(ctr))
    
    if short_question in IGNORE_LIST:
        result = '\\N' # i.e. NULL for MySQL
        # No need to memoize as no expensive computation performed
        return result
    
    # Use composite key of survey_id.short_question.first 20 chars of text_answer
    # Part of text_answer required as certain old values of short_question
    # map to same new short_question
    pkey = '{0}.{1}.{2}'.format(survey_id, short_question, text_answer[0:20])
    
    # If already processed, returned memoized result to save compute
    if pkey in memo_dict:
        return memo_dict[pkey]
    
    # Otherwise, pass to API
    api_ctr += 1
    # Print api_ctr every 100 comments
    if api_ctr % 500 == 0:
        print('{0} new comments passed to API.'.format(api_ctr))
        # API has limit of 500 queries / min
        time.sleep(60)
    try:
        document = language.types.Document(content=text_answer,
                                           type=language.enums.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(document=document).document_sentiment
        # Adjust interval from [-1, 1] to [1, 5]
        # Cast to Decimal then back to int to prevent floating point rounding errors
        result = int(round(Decimal(str((sentiment.score * 2) + 3))))
    # Comments occasionally so badly written the API can't identify the language
    except Exception as e:
        print('Error {0} occurred on sample {1}'.format(e, ctr))
        # Default to overall_satisfaction
        result = float(overall_satisfaction)
    # Memoize and return result
    memo_dict[pkey] = result
    return result

api_results = df.apply(lambda x: get_sentiment_score(x['survey_id'], x['short_question'], x['text_answer'], x['overall_satisfaction']),
                       axis=1,               # Apply to each row
                       raw=False,            # Pass each cell individually as not using NumPy
                       result_type='expand') # Return DataFrame rather than Series of tuples

df['stars'] = api_results

print('3/5: New column created.')

# Export memo_dict to pickle for future re-use
os.chdir(directories.PICKLE_DIR)
with open('memo.pickle', 'wb') as f:
    pickle.dump(memo_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

print('4/5: Pickle exported.')

# Export results as CSV
os.chdir(directories.PROCESSED_DIR)
df.to_csv('comments_processed_ML.csv', sep=',', encoding='utf-8', index=False,
          quotechar='"', line_terminator='\r\n')

# Also export to directory accessible by MySQL
df.to_csv('C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Data\\csps_dashboards\\comments_processed_ML.csv', sep=',', encoding='utf-8', index=False,
          quotechar='"', line_terminator='\r\n')

print('5/5: Data exported.')
