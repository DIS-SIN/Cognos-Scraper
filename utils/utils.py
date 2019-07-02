"""General shared functions and classes."""


def _check_column(col_vals, target_vals):
	"""Compare a column's unique values to target set."""
	for elem in col_vals:
		if elem not in target_vals:
			logger.critical('Failure: Unknown value \'{0}\' in latest Cognos extract.'.format(elem))
			exit()


def _check_col_is_lat_long(my_list):
	"""Ensure values are valid coördinates (i.e. between -180 and 180) or
	a MySQL null (i.e. '\\N').
	"""
	for val in my_list:
		try:
			val_float = float(val)
		except ValueError:
			if val != '\\N':
				return False
		else:
			if not (-180 <= val_float <= 180):
				return False
	return True
