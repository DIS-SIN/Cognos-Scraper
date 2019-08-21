"""Target unique values for select fields in table 'lsr_this_year'. Stored
in Python sets for O(1) lookup times.
"""

BUSINESS_TYPE = {'Instructor-Led', 'Online'}

MONTH_EN = {
	'April',
	'May',
	'June',
	'July',
	'August',
	'September',
	'October',
	'November',
	'December',
	'January',
	'February',
	'March'
}

MONTH_FR = {
	'Avril',
	'Mai',
	'Juin',
	'Juillet',
	'Août',
	'Septembre'
	'Octobre',
	'Novembre',
	'Décembre',
	'Janvier',
	'Février',
	'Mars'
}

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
	'FSL'
}

REGION_EN = {
	'Atlantic',
	'NCR',
	'Online',
	'Ontario Region',
	'Pacific',
	'Prairie',
	'Québec Region',
	'Outside Canada'
}

REGION_FR = {
	'Atlantique',
	'En ligne',
	'Pacifique',
	'Prairie',
	'RCN',
	'Région d\'Ontario',
	'Région du Québec',
	'Hors du Canada'
}

PROVINCE_EN = {
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
	'Unknown',
	'Yukon',
	'Outside Canada'
}

PROVINCE_FR = {
	'Alberta',
	'Colombie-Britannique',
	'En ligne',
	'Île-du-Prince-Édouard',
	'Inconnu',
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

REG_STATUS = {
	'Cancelled',
	'Cancelled - Class Cancelled',
	'Confirmed',
	'Offered',
	'Waitlisted'
}

NO_SHOW = {0, 1}

LEARNER_LANGUAGE = {'English', 'French'}
