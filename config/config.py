import os
from os import path

"""
Logging config
"""
# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.abspath(__file__))
LOGGING_CONFIG = path.join(PROJECT_HOME, 'logging/logging.conf')

"""
RDS
"""
# RDS connection config
CONN_TYPE = "mysql+pymysql"
USER = os.environ.get("MYSQL_USER")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
HOST = os.environ.get("MYSQL_HOST")
PORT = os.environ.get("MYSQL_PORT")
DATABASE = os.environ.get("DATABASE_NAME")
RDS_ENGING_STRING = "{}://{}:{}@{}:{}/{}".format(CONN_TYPE, USER, PASSWORD, HOST, PORT, DATABASE)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")

"""
Local database connection config
"""
LOCAL_DATABASE = "market_basket_analysis.db"
DATABASE_PATH = path.join(path.dirname(PROJECT_HOME), 'data/{}'.format(LOCAL_DATABASE))
LOCAL_ENGING_STRING = 'sqlite:////{}'.format(DATABASE_PATH)



"""
Local file config - which csv file to be uploaded to RDS/Local database
"""
# pseudo file, change later

PRED_FILE = "pred.csv"
TABLE = "prds_rec"

"""
S3
"""

OBJECT_NAME = "online_retail_II.csv"
BUCKET_NAME = "msia423-product-recommendation"
FILE_NAME = "online_retail_II.csv"



