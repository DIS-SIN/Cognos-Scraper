CITY_DICT = {
	'KINGSTON, JAMAICA': 'KINGSTON, JAMAÏQUE',
	'NATIONAL CAPITAL REGION': 'RÉGION DE LA CAPITALE NATIONALE (RCN)',
	'NATIONAL CAPITAL REGION (NCR)': 'RÉGION DE LA CAPITALE NATIONALE (RCN)',
	'Online': 'En ligne'
}


def city_map(my_city):
	"""At the moment, source DB does not contain FR city names. However,
	certain cities require translation e.g. 'NCR'.
	"""
	if my_city in CITY_DICT:
		return CITY_DICT[my_city]
	else:
		return my_city
