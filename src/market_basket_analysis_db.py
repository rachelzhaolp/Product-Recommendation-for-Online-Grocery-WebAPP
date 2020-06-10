import logging.config
import os
import sqlalchemy
import pandas as pd
import config.config as config

logger = logging.getLogger(__name__)


def add_rec(args):
    """Add new records into table.

    Args:
        args: argparse args - should include arg.method, args.file, arg.table
        args.method: (String) How to behave if the table already exists.
        args.file: (String) csv file read the records from
        arg.table: (String) table name

    Returns:None

    """
    try:
        SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
        engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
        logger.info("Successfully connected to the database.")
        df = pd.read_csv(args.file)
        df.to_sql(con=engine, index_label='id', name=config.TABLE, if_exists=args.method)
        logger.info("Successfully uploaded data into prds_rec with " + args.method + " method")
    except Exception as e:
        logger.error("Unexpected error occurred when add records to database: " + str(e))



