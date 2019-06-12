import glob
import os
import time


def _send_email(filename):
	"""On error, send email to project admin."""
	print('We\'re having tremendous problems with: {0}.'.format(filename))


def check_file_exists(filename):
	"""Check every 5 seconds if file exists in current working directory; send
	email on error.
	"""
	ctr = 0
	while not os.path.isfile(filename):
		if ctr == 60:
			_send_email(filename)
			return False
		time.sleep(5)
		ctr += 1
	return True


def delete_files_of_this_ilk(ilk):
	"""Delete 'Foo.xls', 'Foo (1).xls', etc. from current working directory."""
	files = glob.glob('{0}*.xls'.format(ilk))
	for file in files:
		try:
			os.remove(file)
		except FileNotFoundError:
			pass
