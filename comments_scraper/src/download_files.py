"""Download raw data (comments and their associated overall satisfaction scores)
as CSVs from Cognos.
"""
import os
from selenium import webdriver
from comments_scraper.config import deeplinks
from config import shared_deeplinks, shared_directories
from utils.file_system import check_file_exists, delete_files_of_this_ilk

# Cognos login
USERNAME = os.environ.get('COGNOS_USERNAME')
PASSWORD = os.environ.get('COGNOS_PASSWORD')
assert USERNAME is not None, 'Missing USERNAME'
assert PASSWORD is not None, 'Missing PASSWORD'

# Delete previous raw data downloads
os.chdir(shared_directories.DOWNLOADS_DIR)
delete_files_of_this_ilk('Comments')
delete_files_of_this_ilk('Overall Satisfaction')
print('1/7: Previous files deleted.')

# Open controlled browser
browser = webdriver.Chrome()
print('2/7: Browser opened.')

# Navigate to Cognos and login
browser.get(shared_deeplinks.LOGIN_URL)
browser.find_element_by_id('CAMUsername').send_keys(USERNAME)
browser.find_element_by_id('CAMPassword').send_keys(PASSWORD)
browser.find_element_by_id('cmdOK').click()
print('3/7: Logged in to Cognos.')

# Download comments
browser.get(deeplinks.COMMENTS_URL)
os.chdir(shared_directories.DOWNLOADS_DIR)
assert check_file_exists('Comments.xls'), 'Comments download unsuccessful'
print('4/7: Comments downloaded.')

# Download overall satisfaction
browser.get(deeplinks.OVERALL_SATISFACTION_URL)
os.chdir(shared_directories.DOWNLOADS_DIR)
assert check_file_exists('Overall Satisfaction.xls'), 'Overall Satisfaction download unsuccessful'
print('5/7: Overall satisfaction downloaded.')

# Logout
browser.find_elements_by_css_selector('#_NS_logOnOff td')[0].click()
print('6/7: Logged out.')

# End app
browser.quit()
print('7/7: App ended.')
