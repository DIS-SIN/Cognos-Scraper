"""General shared functions and classes."""


def _check_column(col_vals, target_vals):
	"""Compare a column's unique values to target set."""
	for elem in col_vals:
		if elem not in target_vals:
			logger.critical('Failure: Unknown value \'{0}\' in latest Cognos extract.'.format(elem))
			exit()
