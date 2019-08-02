"""Target unique values for select fields in table 'comments'. Stored
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

OFFERING_REGION_EN = {
	'Atlantic',
	'NCR',
	'Online',
	'Ontario Region',
	'Pacific',
	'Prairie',
	'Québec Region'
}

OFFERING_REGION_FR = {
	'Atlantique',
	'En ligne',
	'Pacifique',
	'Prairie',
	'RCN',
	'Région d\'Ontario',
	'Région du Québec',
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
	'Yukon'
}

LEARNER_PROVINCE = {
	'Alberta',
	'British Columbia',
	'Manitoba',
	'NCR/RCN',
	'New Brunswick',
	'Newfoundland and Labrador',
	'Northwest Territories',
	'Nova Scotia',
	'Nunavut',
	'Ontario',
	'Ontario_NCR',
	'Outside Canada',
	'Prince Edward Island',
	'Quebec',
	'Québec_NCR',
	'Saskatchewan',
	'Unknown',
	'Yukon'
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
