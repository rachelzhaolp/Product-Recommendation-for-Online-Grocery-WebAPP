import logging.config

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
import pandas as pd

import config.config as config

Base = declarative_base()
logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('market-basket-analysis-db')


class Rec(Base):
    """Create a data model for the database to be set up product recommendation predictions """

    __tablename__ = 'prds_rec'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(100), unique=False, nullable=False)
    rec1 = Column(String(100), unique=False, nullable=False)
    price1 = Column(Float, unique=False, nullable=False)
    rec2 = Column(String(100), unique=False, nullable=False)
    price2 = Column(Float, unique=False, nullable=False)
    rec3 = Column(String(100), unique=False, nullable=False)
    price3 = Column(Float, unique=False, nullable=False)

    def __repr__(self):
        return "<Rec(Product_ID={}, Product_Name={})>".format(self.id, self.product_name)


def truncate(args):
    """Truncate table

    Args:
        args: argparse args - should include args.table, args.rds
        args.rds: Boolean, True for connecting to RDS, False for connecting to local database
        args.table: String, table to truncate

    Returns:None

    """
    if args.rds:
        engine = sqlalchemy.create_engine(config.RDS_ENGING_STRING)
    else:
        engine = sqlalchemy.create_engine(config.LOCAL_ENGING_STRING)

    logger.info("Successfully connected to the database.")
    maker = sessionmaker(bind=engine)
    session = maker()
    try:
        logger.info("Attempting to truncate table.")
        session.execute("DELETE FROM {}".format(args.table))
        session.commit()
        logger.info("Successfully truncated.")
    except Exception as e:
        logger.error("Error occurred while attempting to truncate table.")
        logger.error(e)
    finally:
        session.close()


def create_db(args):
    """Creates a database

    Args:
        args: argparse args - should include args.rds
        args.rds: Boolean, True for connecting to RDS, False for connecting to local database

    Returns:None

    """
    if args.rds:
        print(config.RDS_ENGING_STRING)
        engine = sqlalchemy.create_engine(config.RDS_ENGING_STRING)
    else:
        engine = sqlalchemy.create_engine(config.LOCAL_ENGING_STRING)

    logger.info("Successfully connected to the database.")
    Base.metadata.create_all(engine)
    logger.info("Finished creating tables.")


"""
add_rec function will be used later to upload data into RDS
"""


def add_rec(args):
    """Add new records into prds_rec.

    Args:
        args: argparse args - should include args.rds, arg.method, args.file
        args.rds: Boolean, True for connecting to RDS, False for connecting to local database
        args.method: String, How to behave if the table already exists.
        args.file: String, csv file read the records from

    Returns:None

    """
    if args.rds:
        engine = sqlalchemy.create_engine(config.RDS_ENGING_STRING)
    else:
        engine = sqlalchemy.create_engine(config.LOCAL_ENGING_STRING)
    logger.info("Successfully connected to the database.")
    df = pd.read_csv(args.file)
    df.to_sql(con=engine, index_label='id', name=Rec.__tablename__, if_exists=args.method)
    logger.info("Successfully uploaded data into prds_rec with " + args.method + " method")
