import os
import mysql.connector

def get_db():
	"""Connect to remote MySQL DB."""
	db = mysql.connector.connect(host=os.environ.get('DB_HOST'),
								 user=os.environ.get('DB_USER'),
								 password=os.environ.get('DB_PASSWORD'),
								 database=os.environ.get('DB_DATABASE_NAME'))
	return db


def run_mysql(cnx, query, args=None):
	"""Run commands on remote MySQL DB."""
	cursor = cnx.cursor()
	cursor.execute(query, args)
	cnx.commit()
	cursor.close()
