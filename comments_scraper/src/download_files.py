"""Download raw data (comments and their associated overall satisfaction scores)
as CSVs from Cognos.
"""
import glob
import os
import time
from selenium import webdriver
from comments_scraper.config import deeplinks, directories

# Cognos login
USERNAME = os.environ.get('COGNOS_USERNAME')
PASSWORD = os.environ.get('COGNOS_PASSWORD')


def send_email(filename):
	"""On error, send email to project admin."""
	print('We\'re having tremendous problems with {0}.'.format(filename))


def check_file_exists(filename):
	"""Check every 5 seconds if file exists in current working directory; send
	email on error.
	"""
	ctr = 0
	while not os.path.isfile(filename):
		if ctr == 60:
			send_email(filename)
			return False
		time.sleep(5)
		ctr += 1
	return True


def delete_files_of_this_ilk(ilk):
	"""Delete 'Comments.xls', 'Comments (1).xls', etc. from current working directory."""
	files = glob.glob('{0}*.xls'.format(ilk))
	for file in files:
		try:
			os.remove(file)
		except FileNotFoundError:
			pass


# Delete previous raw data downloads
os.chdir(directories.DOWNLOADS_DIR)
delete_files_of_this_ilk('Comments')
delete_files_of_this_ilk('Overall Satisfaction')
print('1/7: Previous files deleted.')

# Open controlled browser
browser = webdriver.Chrome()
print('2/7: Browser opened.')

# Navigate to Cognos and login
browser.get(deeplinks.LOGIN_URL)
browser.find_element_by_id('CAMUsername').send_keys(USERNAME)
browser.find_element_by_id('CAMPassword').send_keys(PASSWORD)
browser.find_element_by_id('cmdOK').click()
print('3/7: Logged in to Cognos.')

# Download comments
browser.get(deeplinks.COMMENTS_URL)
assert(check_file_exists('Comments.xls'))
print('4/7: Comments downloaded.')

# Download overall satisfaction
browser.get(deeplinks.OVERALL_SATISFACTION_URL)
assert(check_file_exists('Overall Satisfaction.xls'))
print('5/7: Overall satisfaction downloaded.')

# Logout
browser.find_elements_by_css_selector('#_NS_logOnOff td')[0].click()
print('6/7: Logged out.')

# End app
browser.quit()
print('7/7: App ended.')
