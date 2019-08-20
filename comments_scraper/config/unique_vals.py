"""Target unique values for select fields in table 'comments'. Stored
in Python sets for O(1) lookup times.
"""

QUARTER = {'Q1', 'Q2', 'Q3', 'Q4'}

ORIGINAL_QUESTION = {
	'Comment - General ',
	'Comment - OL Not Available',
	'Comment - application for performance improvement',
	'Comment - general',
	'Comments',
	'Comments  ',
	'Comments for Improvement',
	'Describe technical issues',
	'GCCampus Tools Used',
	'Issue Description',
	'Official Language Available ',
	'Prep - Did not prepare',
	'Prep - Discuss with supervisor',
	'Prep - Job related development',
	'Prep - Pre-course work',
	'Prep - Related courses',
	'Reason to Participate',
	'Technical Issues',
	'Technical Issues?',
	# New questions from Nanos survey
	'2. Satisfaction Overall Comments',
	'8. Technical Experience',
	'24. Comments you would like to share to help the School improve'
}
