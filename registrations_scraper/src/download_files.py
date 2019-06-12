"""Download LSR (i.e. registrations) as CSV from Cognos."""
import os
from selenium import webdriver
from config import deeplinks, directories
from config.utils import check_file_exists, delete_files_of_this_ilk

# Cognos login
USERNAME = os.environ.get('COGNOS_USERNAME')
PASSWORD = os.environ.get('COGNOS_PASSWORD')

# Delete previous raw data downloads
os.chdir(directories.DOWNLOADS_DIR)
delete_files_of_this_ilk('LSR Mini')
print('1/6: Previous files deleted.')

# Open controlled browser
browser = webdriver.Chrome()
print('2/6: Browser opened.')

# Navigate to Cognos and login
browser.get(deeplinks.LOGIN_URL)
browser.find_element_by_id('CAMUsername').send_keys(USERNAME)
browser.find_element_by_id('CAMPassword').send_keys(PASSWORD)
browser.find_element_by_id('cmdOK').click()
print('3/6: Logged in to Cognos.')

# Download LSR
browser.get(deeplinks.LSR_URL)
os.chdir(directories.DOWNLOADS_DIR)
assert(check_file_exists('LSR Mini.xls'))
print('4/6: LSR downloaded.')

# Logout
browser.find_elements_by_css_selector('#_NS_logOnOff td')[0].click()
print('5/6: Logged out.')

# End app
browser.quit()
print('6/6: Browser closed.')
