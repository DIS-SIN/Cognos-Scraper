import os
import mysql.connector
from comments_scraper.config.preferences import LOCAL_DB

# Global var in which to store DB connection
db = None


def get_db(local):
    global db
    if db is None:
        if local:
            db = mysql.connector.connect(host='localhost',
                                         user='admin',
                                         password=os.environ.get('DB_PASSWORD'),
                                         database=os.environ.get('DB_DATABASE_NAME'))
        else:
            db = mysql.connector.connect(host=os.environ.get('DB_HOST'),
                                         user=os.environ.get('DB_USER'),
                                         password=os.environ.get('DB_PASSWORD'),
                                         database=os.environ.get('DB_DATABASE_NAME'))
    return db


def run_mysql(query, args=None):
    """Run commands via connection in global var 'db'."""
    cnx = get_db(LOCAL_DB)
    cursor = cnx.cursor()
    cursor.execute(query, args)
    cnx.commit()
    cursor.close()

drop_existing_table = """
    DROP TABLE IF EXISTS comments;
"""

create_table = """
    CREATE TABLE comments(
        course_code VARCHAR(20),
        survey_id VARCHAR(15),
        fiscal_year VARCHAR(9),
        quarter VARCHAR(5),
        learner_classif VARCHAR(80),
        offering_city_en VARCHAR(60),
        short_question VARCHAR(60),
        text_answer TEXT,
        offering_city_fr VARCHAR(60),
        text_answer_fr VARCHAR(90),
        overall_satisfaction TINYINT,
        stars TINYINT
    );
"""

load_data = """
    LOAD DATA INFILE 'comments_processed_ML.csv'
    INTO TABLE comments
    FIELDS OPTIONALLY ENCLOSED BY '"'
    TERMINATED BY ','
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES;
"""

create_index = """
    CREATE INDEX idx_cc_sq ON comments(course_code, short_question);
"""

try:
    run_mysql(drop_existing_table)
    run_mysql(create_table)
    run_mysql(load_data)
    run_mysql(create_index)
except Exception as e:
    print('We\'re having tremendous problems with:', e)
else:
    print('1/1: Data pushed to MySQL.')
finally:
    db.close()
