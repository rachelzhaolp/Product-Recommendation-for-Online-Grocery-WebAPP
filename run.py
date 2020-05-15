import argparse
import config.config as config

from src.interact_s3 import upload_file, download_file
from src.market_basket_analysis_db import truncate, create_db, add_rec

if __name__ == '__main__':
    # Add parsers for both creating a database and adding songs to it
    parser = argparse.ArgumentParser(description="Build data pipeline for msia423 project")
    subparsers = parser.add_subparsers()

    # Sub-parser for uploading file to S3 bucket
    sb_upload = subparsers.add_parser("upload_file", description="Upload file from local to S3 bucket")
    sb_upload.add_argument("--file_name", default=config.FILE_NAME, help="file to upload")
    sb_upload.add_argument("--bucket_name", default=config.BUCKET_NAME, help="S3 bucket name to upload into")
    sb_upload.add_argument("--object_name", default=config.OBJECT_NAME, help=" object name of the uploaded file")
    sb_upload.set_defaults(func=upload_file)

    # Sub-parser for downloading file from S3 bucket
    sb_download = subparsers.add_parser("download_file", description="Download file from S3 bucket to local")
    sb_download.add_argument("--object_name", default=config.OBJECT_NAME, help=" object to download")
    sb_download.add_argument("--bucket_name", default=config.BUCKET_NAME, help="S3 bucket to download from")
    sb_download.add_argument("--file_name", default=config.FILE_NAME, help="filename of the downloaded object")
    sb_download.set_defaults(func=download_file)

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--rds", default=False, help="Boolean, True for connecting to RDS, False for connecting "
                                                        "to local database")
    sb_create.set_defaults(func=create_db)

    """
    sb_add and sb_truncate will not be used later when we insert data into RDS.
    """
    # Sub-parser for add records to a table in RDS/Local sqlite
    sb_add = subparsers.add_parser("add_rec", description="Add records to a table table")
    sb_add.add_argument("--rds", default=False, help="Boolean, True for connecting to RDS, False for connecting "
                                                     "to local database")
    sb_add.add_argument("--file", default=config.PRED_FILE, help="Which file to write into the prds_rec table")
    sb_add.add_argument("--method", default="replace", choices={"fail", "replace", "append"},
                        help="How to behave if the table already exists."
                             "fail: Raise a ValueError."
                             "replace: Drop the table before inserting new values."
                             "append: Insert new values to the existing table.")
    sb_add.set_defaults(func=add_rec)

    # Sub-parser for truncate a table
    sb_truncate = subparsers.add_parser("truncate_db", description="truncate table")
    sb_truncate.add_argument("--rds", default=False, help="Boolean, True for connecting to RDS, False for connecting "
                                                          "to local database")
    sb_truncate.add_argument("--table", default=config.TABLE, help="Which table to truncate")
    sb_truncate.set_defaults(func=truncate)

    args = parser.parse_args()
    args.func(args)
