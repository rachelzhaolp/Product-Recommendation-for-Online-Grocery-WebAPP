import os
import config.config as config

DEBUG = True  # Keep True for debugging, change to False when moving to production
HOST = "0.0.0.0"  # the host that is running the app. 0.0.0.0 when running locally
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')  # URI (engine string) for database that contains tracks
APP_NAME = "Rachel's Grocery Store"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

if SQLALCHEMY_DATABASE_URI is not None:
    pass
elif config.MYSQL_HOST is None:
    SQLALCHEMY_DATABASE_URI = config.LOCAL_ENGING_STRING
else:
    SQLALCHEMY_DATABASE_URI = config.RDS_ENGING_STRING
