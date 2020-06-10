import os
import config.config as config

DEBUG = False  # Keep True for debugging, change to False when moving to production
HOST = "0.0.0.0"  # the host that is running the app. 0.0.0.0 when running locally
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile
APP_NAME = "Rachel's Grocery Store"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # URI (engine string) for database that contains the recommendations

if SQLALCHEMY_DATABASE_URI is not None:
    pass
else:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://msia423instructor:lzp2080@market-basket-analysis.cc1aqge2v9qi.us-west-1.rds.amazonaws.com:3306/prod_rec"

