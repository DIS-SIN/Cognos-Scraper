"""Target unique values for select fields in table 'lsr_this_year'. Stored
in Python sets for O(1) lookup times.
"""

# Table 'registrations' excludes events, unlike table 'offerings'
BUSINESS_TYPE = {'Instructor-Led', 'Online'}

LEARNER_LANGUAGE = {'English', 'French'}

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
	'Septembre',
	'Octobre',
	'Novembre',
	'Décembre',
	'Janvier',
	'Février',
	'Mars'
}

NO_SHOW = {0, 1}

REG_STATUS = {
	'Cancelled',
	'Cancelled - Class Cancelled',
	'Confirmed',
	'Offered',
	'Waitlisted'
}
