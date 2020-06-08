import os
from os import path
PROJECT_HOME = path.dirname(path.abspath(__file__))


"""
config for default path arguments in run.py
"""
# config
CONFIG_YAML = "config/config.yaml"
# raw data
RAW_DATA = "data/online_retail_II.csv"
OBJECT_NAME = "online_retail_II.csv"
BUCKET_NAME = "msia423-product-recommendation"
# clean data
CLEAN_DATA = "data/clean_data.csv"
# basket
BASKETS = "data/basket.csv"
# product_dim
PRODUCT_DIM = "data/product_dim.csv"
# train/test
TRAIN_DATA = "data/training_data.csv"
TEST_DATA = "data/test_data.csv"
# recommendations
REC_PATH = "data/rec.csv"
# evaluation
AUC_ACCURACY_PATH = "evaluations/accuracy.csv"
# eda
FIGURE_PATH = "figures/"


"""
RDS
"""
# RDS connection config
CONN_TYPE = "mysql+pymysql"
USER = os.environ.get("MYSQL_USER")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_PORT = os.environ.get("MYSQL_PORT")
DATABASE = os.environ.get("DATABASE_NAME")
RDS_ENGING_STRING = "{}://{}:{}@{}:{}/{}".format(CONN_TYPE, USER, PASSWORD, MYSQL_HOST, MYSQL_PORT, DATABASE)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

TABLE = 'prods_recs'

"""
Local database connection config
"""

LOCAL_DATABASE = "market_basket_analysis.db"
DATABASE_PATH = path.join(path.dirname(PROJECT_HOME), 'data/{}'.format(LOCAL_DATABASE))
LOCAL_ENGING_STRING = 'sqlite:////{}'.format(DATABASE_PATH)