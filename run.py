import argparse
import logging
import config.config as config
from src.acquire import main as acquire
from src.clean import main as clean
from src.product_dim import main as product_dim
from src.create_basket import main as create_basket
from src.split import main as split
from src.train import main as train
from src.evaluate import main as evaluate
from src.upload_s3 import upload_file
from src.market_basket_analysis_db import add_rec
from test.reproducibility_test import reproducibility_tests

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Add parser for the model pipeline
    parser = argparse.ArgumentParser(description="Model pipeline: acquire data, clean data, create features, train "
                                                 "model, evaluate model and EDA")
    subparsers = parser.add_subparsers()

    # Acquire parser
    sb_acquire = subparsers.add_parser("acquire", description="Acquire data from a S3 bucket and store the raw data "
                                                              "in local file")
    sb_acquire.add_argument('--config', default=config.CONFIG_YAML, help='Path to yaml configuration file')
    sb_acquire.add_argument('--output', '-o', default=config.RAW_DATA, help='Path to save output (optional)')
    sb_acquire.add_argument("--object_name", default=config.OBJECT_NAME, help="Object to download")
    sb_acquire.add_argument("--bucket_name", default=config.BUCKET_NAME, help="S3 bucket to download from")
    sb_acquire.set_defaults(func=acquire)

    # Clean parser
    sb_clean = subparsers.add_parser("clean",
                                     description="Load data from data_source and save cleaned data to out_filepath")
    sb_clean.add_argument('--config', default=config.CONFIG_YAML, help='Path to yaml configuration file')
    sb_clean.add_argument('--input', '-i', default=config.RAW_DATA, help='Path to input data')
    sb_clean.add_argument('--output', '-o', default=config.CLEAN_DATA, help='Path to save output (optional)')
    sb_clean.set_defaults(func=clean)

    # product_dim parser
    sb_product_dim = subparsers.add_parser("product_dim",
                                           description="Create objects table for the products")
    sb_product_dim.add_argument('--config', default=config.CONFIG_YAML, help='Path to yaml configuration file')
    sb_product_dim.add_argument('--input', '-i', default=config.CLEAN_DATA, help='Path to input data')
    sb_product_dim.add_argument('--output', '-o', default=config.PRODUCT_DIM, help='Path to save output (optional)')
    sb_product_dim.set_defaults(func=product_dim)

    # create_basket parser
    sb_product_dim = subparsers.add_parser("create_basket",
                                           description="Create objects table for the products")
    sb_product_dim.add_argument('--config', default=config.CONFIG_YAML, help='Path to yaml configuration file')
    sb_product_dim.add_argument('--input', '-i', default=config.CLEAN_DATA, help='Path to input data')
    sb_product_dim.add_argument('--output', '-o', default=config.BASKETS, help='Path to save output (optional)')
    sb_product_dim.set_defaults(func=create_basket)

    # split parser
    sb_split = subparsers.add_parser("split",
                                     description="Split and store the training/test data")
    sb_split.add_argument('--config', default=config.CONFIG_YAML, help='Path to yaml configuration file')
    sb_split.add_argument('--input', '-i', default=config.BASKETS, help='Path to input data')
    sb_split.add_argument('--output_train', default=config.TRAIN_DATA, help='Path to save training data (optional)')
    sb_split.add_argument('--output_test', default=config.TEST_DATA, help='Path to save test data (optional)')
    sb_split.set_defaults(func=split)

    # train parser
    sb_train = subparsers.add_parser("train",
                                     description="Create objects table for the products")
    sb_train.add_argument('--config', default=config.CONFIG_YAML, help='Path to yaml configuration file')
    sb_train.add_argument('--input', '-i', default=config.TRAIN_DATA, help='Path to input data')
    sb_train.add_argument('--output', '-o', default=config.REC_PATH, help='Path to save output (optional)')
    sb_train.set_defaults(func=train)

    # evaluation parser
    sb_eval = subparsers.add_parser("evaluate",
                                     description="Split and store the training/test data")
    sb_eval.add_argument('--rec', '-r', default=config.REC_PATH, help='Path to input data')
    sb_eval.add_argument('--test', '-t', default=config.TEST_DATA, help='Path to save test data (optional)')
    sb_eval.add_argument('--output', default=config.AUC_ACCURACY_PATH, help='Path to save training data (optional)')
    sb_eval.set_defaults(func=evaluate)

    # Sub-parser for uploading file to S3 bucket
    sb_upload = subparsers.add_parser("upload_file", description="Upload file from local to S3 bucket")
    sb_upload.add_argument("--file_name", default=config.RAW_DATA, help="file to upload")
    sb_upload.add_argument("--bucket_name", default=config.BUCKET_NAME, help="S3 bucket name to upload into")
    sb_upload.add_argument("--object_name", default=config.OBJECT_NAME, help=" object name of the uploaded file")
    sb_upload.set_defaults(func=upload_file)

    # Sub-parser for add records to a table in RDS/Local sqlite
    sb_add = subparsers.add_parser("add_rec", description="Add records to a table table")
    sb_add.add_argument("--rds", default=False, help="Boolean, True for connecting to RDS, False for connecting "
                                                     "to local database")
    sb_add.add_argument("--file", default=config.REC_PATH, help="Which file to write into the prds_rec table")
    sb_add.add_argument("--method", default="replace", choices={"fail", "replace", "append"},
                        help="How to behave if the table already exists."
                             "fail: Raise a ValueError."
                             "replace: Drop the table before inserting new values."
                             "append: Insert new values to the existing table.")
    sb_add.set_defaults(func=add_rec)

    # Sub-parser for conducting reproducibility test
    sb_reproducibility_test = subparsers.add_parser("reproducibility_tests",
                                                    description="Run reproducibility tests")
    sb_reproducibility_test.add_argument('--config', default='test/reproducibility_test.yaml',
                                         help='Path to yaml configuration file')
    sb_reproducibility_test.set_defaults(func=reproducibility_tests)

    args = parser.parse_args()
    args.func(args)
