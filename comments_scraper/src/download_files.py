"""Download raw data (comments and their associated overall satisfaction scores)
as CSVs from Cognos.
"""
import os
from pyvirtualdisplay import Display
from selenium import webdriver
from config import shared_directories
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
print('1/8: Previous files deleted.')

# Open virtual viewport
display = Display(visible=0, size=(1920, 1080))
display.start()
print('2/8: Virtual viewport opened.')

# Open controlled browser
browser = webdriver.Chrome()
print('3/8: Browser opened.')

# Navigate to Cognos and login
browser.get(os.environ.get('LOGIN_URL'))
browser.find_element_by_id('CAMUsername').send_keys(USERNAME)
browser.find_element_by_id('CAMPassword').send_keys(PASSWORD)
browser.find_element_by_id('cmdOK').click()
print('4/8: Logged in to Cognos.')

# Download comments
browser.get(os.environ.get('COMMENTS_URL'))
os.chdir(shared_directories.DOWNLOADS_DIR)
assert check_file_exists('Comments.xls'), 'Comments download unsuccessful'
print('5/8: Comments downloaded.')

# Download overall satisfaction
browser.get(os.environ.get('OVERALL_SATISFACTION_URL'))
os.chdir(shared_directories.DOWNLOADS_DIR)
assert check_file_exists('Overall Satisfaction.xls'), 'Overall Satisfaction download unsuccessful'
print('6/8: Overall satisfaction downloaded.')

# Logout
browser.find_elements_by_css_selector('#_NS_logOnOff td')[0].click()
print('7/8: Logged out of Cognos.')

# End app
browser.quit()
display.stop()
print('8/8: App ended.')
