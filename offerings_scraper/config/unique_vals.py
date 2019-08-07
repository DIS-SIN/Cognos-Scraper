"""Target unique values for select fields in table 'offerings'. Stored
in Python sets for O(1) lookup times.
"""

BUSINESS_TYPE = {'Events', 'Instructor-Led', 'Online'}

QUARTER = {'Q1', 'Q2', 'Q3', 'Q4'}

OFFERING_STATUS = {
	'Cancelled - Normal',
	'Delivered - Normal',
	'N/a',
	'Open - Normal'
}

OFFERING_LANGUAGE = {
	'Bilingual',
	'English',
	'ESL',
	'French',
	'FSL',
	'Simultaneous Translation '
}

OFFERING_REGION_EN = {
	'Atlantic',
	'NCR',
	'Online',
	'Ontario Region',
	'Pacific',
	'Prairie',
	'Québec Region',
	'Outside Canada'
}

OFFERING_REGION_FR = {
	'Atlantique',
	'En ligne',
	'Pacifique',
	'Prairie',
	'RCN',
	'Région d\'Ontario',
	'Région du Québec',
	'Hors du Canada'
}

OFFERING_PROVINCE_EN = {
	'Alberta',
	'British Columbia',
	'Manitoba',
	'NCR/RCN',
	'New Brunswick',
	'Newfoundland and Labrador',
	'Northwest Territories',
	'Nova Scotia',
	'Nunavut',
	'Online',
	'Ontario',
	'Prince Edward Island',
	'Quebec',
	'Saskatchewan',
	'Yukon',
	'Outside Canada'
}

OFFERING_PROVINCE_FR = {
	'Alberta',
	'Colombie-Britannique',
	'Île-du-Prince-Édouard',
	'Manitoba',
	'NCR/RCN',
	'Nouveau-Brunswick',
	'Nouvelle-Écosse',
	'Nunavut',
	'Ontario',
	'Québec',
	'Saskatchewan',
	'Terre-Neuve-et-Labrador',
	'Territoires du Nord-Ouest',
	'Yukon',
	'Hors du Canada'
}
