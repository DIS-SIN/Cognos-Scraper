"""Push processed extract to cloud DB."""
import logging
from registrations_scraper.config.directories import PROCESSED_DIR
from utils.db import get_db, run_mysql

# Instantiate logger
logger = logging.getLogger(__name__)

# Store DB connection in global var to avoid reconnecting after each query
cnx = get_db()
logger.debug('1/7: Connected to DB.')

# MySQL requires paths with forward slashes
PROCESSED_DIR = PROCESSED_DIR.replace('\\', '/')

create_table = """
	CREATE TABLE new_regs(
		course_title_en VARCHAR(200),
		course_title_fr VARCHAR(300),
		course_code VARCHAR(20),
		business_type VARCHAR(30),
		offering_id INT,
		start_date DATE,
		end_date DATE,
		month_en VARCHAR(10),
		month_fr VARCHAR(10),
		client VARCHAR(50),
		offering_status VARCHAR(30),
		offering_language VARCHAR(50),
		offering_region_en VARCHAR(30),
		offering_region_fr VARCHAR(30),
		offering_province_en VARCHAR(30),
		offering_province_fr VARCHAR(30),
		offering_city VARCHAR(50),
		learner_province VARCHAR(30),
		learner_city VARCHAR(50),
		reg_id INT PRIMARY KEY,
		reg_status VARCHAR(30),
		no_show INT,
		learner_id VARCHAR(22),
		learner_language VARCHAR(10),
		learner_classif VARCHAR(40),
		billing_dept_name_en VARCHAR(150),
		billing_dept_name_fr VARCHAR(200),
		offering_city_fr VARCHAR(50),
		learner_city_fr VARCHAR(50),
		offering_lat FLOAT,
		offering_lng FLOAT,
		learner_lat FLOAT,
		learner_lng FLOAT
	);
"""

load_data = """
	LOAD DATA LOCAL INFILE '{0}/lsr_processed_geo.csv'
	INTO TABLE new_regs
	FIELDS OPTIONALLY ENCLOSED BY '"'
	TERMINATED BY ','
	LINES TERMINATED BY '\r\n'
	IGNORE 1 LINES
	(course_title_en, course_title_fr, course_code, business_type, offering_id, @temp_start_date, @temp_end_date, month_en, month_fr, client, offering_status, offering_language, offering_region_en, offering_region_fr, offering_province_en, offering_province_fr, offering_city, learner_province, learner_city, reg_id, reg_status, no_show, learner_id, learner_language, learner_classif, billing_dept_name_en, billing_dept_name_fr, offering_city_fr, learner_city_fr, offering_lat, offering_lng, learner_lat, learner_lng)
	SET start_date = STR_TO_DATE(@temp_start_date, '%Y-%m-%d %T'),
	end_date = STR_TO_DATE(@temp_end_date, '%Y-%m-%d %T');
""".format(PROCESSED_DIR)

indices = [
	# Index for selection page
	'CREATE INDEX idx_cc_cten ON new_regs(course_code, course_title_en);',
	'CREATE INDEX idx_cc_ctfr ON new_regs(course_code, course_title_fr);',
	'CREATE INDEX idx_cten_cc ON new_regs(course_title_en, course_code);',
	
	# Index for open, delivered, cancelled offerings
	'CREATE INDEX idx_cc_os_oid ON new_regs(course_code, offering_status, offering_id);',
	
	# Index for client requests
	'CREATE INDEX idx_cc_cl_os_oid ON new_regs(course_code, client, offering_status, offering_id);',
	
	# Index for confirmed regs
	'CREATE INDEX idx_cc_rs ON new_regs(course_code, reg_status);',
	
	# Index for total no-shows
	'CREATE INDEX idx_cc_ns ON new_regs(course_code, no_show);',
	
	# Index for combo no-shows and registrations per month
	'CREATE INDEX idx_cc_mnen_rs_ns ON new_regs(course_code, month_en, reg_status, no_show);',
	'CREATE INDEX idx_cc_mnfr_rs_ns ON new_regs(course_code, month_fr, reg_status, no_show);',
	
	# Index for class OfferingLocations
	'CREATE INDEX idx_cc_os_oren_open_oc_oid ON new_regs(course_code, offering_status, offering_region_en, offering_province_en, offering_city, offering_id);',
	'CREATE INDEX idx_cc_os_orfr_opfr_oc_oid ON new_regs(course_code, offering_status, offering_region_fr, offering_province_fr, offering_city, offering_id);',
	
	# Index for offerings per language
	'CREATE INDEX idx_cc_os_ol_oid ON new_regs(course_code, offering_status, offering_language, offering_id);',
	
	# Index for offerings cancelled
	# None needed, already runs in 0.0s
	
	# Index for offerings cancelled global
	'CREATE INDEX idx_bt_os_oid ON new_regs(business_type, offering_status, offering_id);',
	
	# Index for top 5 departments
	'CREATE INDEX idx_cc_rs_bdnen ON new_regs(course_code, reg_status, billing_dept_name_en);',
	'CREATE INDEX idx_cc_rs_bdnfr ON new_regs(course_code, reg_status, billing_dept_name_fr);',
	
	# Index for top 5 classifications
	'CREATE INDEX idx_cc_rs_lc ON new_regs(course_code, reg_status, learner_classif);',
	
	# Index for average class size
	'CREATE INDEX idx_cc_rs_oid ON new_regs(course_code, reg_status, offering_id);',
	
	# Index for average class size global
	'CREATE INDEX idx_rs_bt_oid ON new_regs(reg_status, business_type, offering_id);',
	
	# Index for average no-shows
	# None needed, already runs in 0.0s
	
	# Index for average no-shows global
	'CREATE INDEX idx_ns ON new_regs(no_show);',
	
	# Index for offering city counts
	'CREATE INDEX idx_cc_os_oc_olat_olng_oid ON new_regs(course_code, offering_status, offering_city, offering_lat, offering_lng, offering_id);',
	
	# Index for learner city counts
	'CREATE INDEX idx_cc_rs_lc_llat_llng_lid ON new_regs(course_code, reg_status, learner_city, learner_lat, learner_lng, learner_id);',
	
	# Index for regs per month
	'CREATE INDEX idx_cc_rs_mnen ON new_regs(course_code, reg_status, month_en);',
	'CREATE INDEX idx_cc_rs_mnfr ON new_regs(course_code, reg_status, month_fr);',
	
	# Index for REGISTHOR: learner_city and learner_province
	'CREATE INDEX idx_lc_lp ON new_regs(learner_city, learner_province);',
	
	# Index for REGISTHOR: learner_classif
	'CREATE INDEX idx_lclassif ON new_regs(learner_classif);',
	
	# Index for REGISTHOR: billing_dept_name
	'CREATE INDEX idx_bdnen ON new_regs(billing_dept_name_en);',
	'CREATE INDEX idx_bdnfr ON new_regs(billing_dept_name_fr);'
]

# Rename tables in a single atomic transaction
# Ensures clean switchover + no downtime
rename_tables = """
	RENAME TABLE lsr_this_year TO old_regs, new_regs TO lsr_this_year;
"""

drop_table = """
	DROP TABLE old_regs;
"""

try:
	run_mysql(cnx, create_table)
	logger.debug('2/7: New table created.')
	run_mysql(cnx, load_data)
	logger.debug('3/7: Data loaded.')
	for index in indices:
		run_mysql(cnx, index)
	logger.debug('4/7: Indices created.')
	run_mysql(cnx, rename_tables)
	logger.debug('5/7: Tables renamed.')
	run_mysql(cnx, drop_table)
	logger.debug('6/7: Old table dropped.')
except Exception as e:
	logger.critical('Failure!', exc_info=True)
	cnx.close()
	exit()
finally:
	cnx.close()
	logger.debug('7/7: Connection closed.')
