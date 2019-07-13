"""Target unique values for select fields in table 'offerings'. Stored
in Python sets for O(1) lookup times.
"""

BUSINESS_TYPE = {'Events', 'Instructor-Led', 'Online'}

OFFERING_STATUS = {
	'Cancelled - Normal',
	'Delivered - Normal',
	'N/a',
	'Open - Normal'
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
