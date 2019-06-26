"""Geocode offering and learner locations with the Google Geocoding API."""
import json
import logging
import os
import pickle
import requests
import urllib
import pandas as pd
from config import shared_directories
from registrations_scraper.config import directories

# Instantiate logger
logger = logging.getLogger(__name__)

# Check if credentials stored in environ vars
API_KEY = os.environ.get('GOOGLE_GEOCODING_KEY', None)
if API_KEY is None:
    logger.critical('Failure: Missing Google NLP API credentials.')
    exit()

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

logger.info('1/5: Data imported.')

# Load pickle for memoization
os.chdir(directories.PICKLE_DIR)
with open('geo_dict.pickle', 'rb') as f:
    geo_dict = pickle.load(f)

logger.info('2/5: Pickle imported.')

# New cities passed to API
api_ctr = 0


def _get_memo_name(city, prov):
    """Create composite key of format 'City, Province' for memoization."""
    return '{0}, {1}'.format(city, prov)


def _get_lookup_name(city, prov):
    """Remove junk strings that interfere with Geocoding API"""
    return '{0}, {1}'.format(city, prov).replace(', Outside Canada', '').replace('_NCR', '')


def get_lat_lng(city, prov):
    """
    Get a city's latitude and longitude from the Google Maps Geocoding API and memoize.
    """
    # Format city name for memoization
    memo_city = _get_memo_name(city, prov)
    
    # Format city name for API
    lookup_city = _get_lookup_name(city, prov)
    
    # Memoization
    global geo_dict
    if memo_city in geo_dict:
        return geo_dict[memo_city]
    
    # Build query; use urllib to properly encode non-ASCII chars
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    url_vars = {'address': lookup_city, 'key': API_KEY, 'region': 'ca'}
    my_query = url + urllib.parse.urlencode(url_vars)
    geo_request = requests.get(my_query)
    
    # Check if request was successful
    if geo_request.status_code == 200:
        geo_response = json.loads(geo_request.text)
    else:
        logger.warning('Request error with city {0}: {1}'.format(lookup_city, geo_request.status_code))
    
    # Check if API response status is 'OK'
    api_status = geo_response['status']
    if api_status != 'OK':
        logger.warning('API error with city {0}: {1}'.format(lookup_city, api_status))
    
    # Parse results and memoize
    lat = geo_response['results'][0]['geometry']['location']['lat']
    lng = geo_response['results'][0]['geometry']['location']['lng']
    results = {'lat': lat, 'lng': lng}
    geo_dict[memo_city] = results
    global api_ctr
    api_ctr += 1
    logger.info('New city geocoded: {0} at {1}, {2}.'.format(lookup_city, lat, lng))
    
    return results

# Add offering latitude and longitude
regs['offering_lat'] = regs.apply(lambda x: get_lat_lng(x['offering_city'], x['offering_province_en'])['lat'], axis=1)
regs['offering_lng'] = regs.apply(lambda x: get_lat_lng(x['offering_city'], x['offering_province_en'])['lng'], axis=1)

# Add learner latitude and longitude
regs['learner_lat'] = regs.apply(lambda x: get_lat_lng(x['learner_city'], x['learner_province'])['lat'], axis=1)
regs['learner_lng'] = regs.apply(lambda x: get_lat_lng(x['learner_city'], x['learner_province'])['lng'], axis=1)

logger.info('3/5: New columns created.')

# Export geo_dict to pickle for future re-use
os.chdir(directories.PICKLE_DIR)
with open('geo_dict.pickle', 'wb') as f:
    pickle.dump(geo_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

logger.info('4/5: Pickle exported.')

# Export results as CSV
os.chdir(directories.PROCESSED_DIR)
regs.to_csv('lsr_processed.csv', sep=',', encoding='utf-8', index=False,
            quotechar='"', line_terminator='\r\n')

logger.info('5/5: Data exported.')
