"""Geocode offering and learner locations with the Google Geocoding API."""
import json
import logging
import os
import pickle
import requests
import urllib
import pandas as pd
from utils.utils import _check_col_in_valid_range
from registrations_scraper.config import directories

# Instantiate logger
logger = logging.getLogger(__name__)

# Check if credentials stored in environ vars
API_KEY = os.environ.get('GOOGLE_GEOCODING_KEY', None)
if API_KEY is None:
	logger.critical('Failure: Missing Google NLP API credentials.')
	exit()

### IMPORT RAW DATA ###
os.chdir(directories.PROCESSED_DIR)
regs = pd.read_csv('lsr_processed.csv', sep=',', index_col=False, encoding='utf-8',
				   keep_default_na=False)
if not regs.shape[0] > 0:
	logger.critical('Failure: lsr_processed.csv is empty.')
	exit()

logger.debug('1/5: Data imported.')

# Load pickle for memoization
os.chdir(directories.PICKLE_DIR)
with open('geo_dict.pickle', 'rb') as f:
	geo_dict = pickle.load(f)

logger.debug('2/5: Pickle imported.')

# New cities passed to API
new_ctr = 0

# New cities that failed to geocode/json
fail_ctr = 0


def _get_memo_name(city, prov):
	"""Create composite key of format 'City, Province' for memoization."""
	return '{0}, {1}'.format(city, prov)


def _get_lookup_name(city, prov):
	"""Remove junk strings that interfere with Geocoding API"""
	return '{0}, {1}'.format(city, prov).replace(', Outside Canada', '').replace(', Unknown', '')


def get_lat_lng(city, prov):
	"""
	Get a city's latitude and longitude from the Google Maps Geocoding API and memoize.
	"""
	global fail_ctr
	global geo_dict
	global new_ctr
	
	# Format city name for memoization
	memo_city = _get_memo_name(city, prov)
	
	# Format city name for API
	lookup_city = _get_lookup_name(city, prov)
	
	# Memoization
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
		fail_ctr += 1
		if fail_ctr >= 3:
			exit()
	
	# Check if API response status is 'OK'
	api_status = geo_response['status']
	if api_status != 'OK':
		logger.warning('API error with city {0}: {1}'.format(lookup_city, api_status))
		fail_ctr += 1
		if fail_ctr >= 3:
			exit()
	
	# Parse results and memoize
	lat = geo_response['results'][0]['geometry']['location']['lat']
	lng = geo_response['results'][0]['geometry']['location']['lng']
	results = {'lat': lat, 'lng': lng}
	geo_dict[memo_city] = results
	new_ctr += 1
	logger.info('New city geocoded: {0} at {1}, {2}.'.format(lookup_city, lat, lng))
	
	return results

# Add offering latitude and longitude
regs['offering_lat'] = regs.apply(lambda x: get_lat_lng(x['offering_city_en'], x['offering_province_en'])['lat'], axis=1)
regs['offering_lng'] = regs.apply(lambda x: get_lat_lng(x['offering_city_en'], x['offering_province_en'])['lng'], axis=1)

# Add learner latitude and longitude
regs['learner_lat'] = regs.apply(lambda x: get_lat_lng(x['learner_city_en'], x['learner_province_en'])['lat'], axis=1)
regs['learner_lng'] = regs.apply(lambda x: get_lat_lng(x['learner_city_en'], x['learner_province_en'])['lng'], axis=1)

# Ensure new columns contain valid coördinates
if not _check_col_in_valid_range(regs['offering_lat'].unique(), -180, 180) and \
	   _check_col_in_valid_range(regs['offering_lng'].unique(), -180, 180) and \
	   _check_col_in_valid_range(regs['learner_lat'].unique(), -180, 180) and \
	   _check_col_in_valid_range(regs['learner_lng'].unique(), -180, 180):
	logger.critical('Failure: Invalid coördinates.')
	exit()

logger.debug('3/5: New columns created.')

# Export geo_dict to pickle for future re-use
os.chdir(directories.PICKLE_DIR)
with open('geo_dict.pickle', 'wb') as f:
	pickle.dump(geo_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

logger.debug('4/5: Pickle exported.')

# Export results as CSV
os.chdir(directories.PROCESSED_DIR)
regs.to_csv('lsr_processed_geo.csv', sep=',', encoding='utf-8', index=False,
			quotechar='"', line_terminator='\r\n')

logger.debug('5/5: Data exported.')
