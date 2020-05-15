import logging.config
from os import path
import boto3
from botocore.exceptions import ClientError

import config.config as config

logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('interact-s3')


def upload_file(args):
    """Upload a file to an S3 bucket

    Args:
        args: argparse args - should include args.file_name, args.bucket_name, args.object_name
        args.file_name: String, file to upload
        args.bucket_name: String, S3 bucket to upload into
        args.object_name: String, object name of the uploaded file

    Returns: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if args.object_name is None:
        args.object_name = args.file_name

    file_path = path.join(path.dirname(config.PROJECT_HOME), 'data/{}'.format(args.file_name))

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, args.bucket_name, args.object_name)
        logging.info("Successfully uploaded " + args.file_name + " to " + args.bucket_name + " S3 bucket")
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(args):
    """Download a file from an S3 bucket

    Args:
        args: argparse args - should include args.object_name, args.bucket_name, args.file_name
        args.object_name: String, object to download
        args.bucket_name: String, S3 bucket to download from
        args.file_name: String, filename of the downloaded object

    Returns: True if object was downloaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if args.file_name is None:
        args.file_name = args.object_name
    file_path = path.join(path.dirname(config.PROJECT_HOME), 'data/{}'.format(args.file_name))

    # Upload the file
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(args.bucket_name).download_file(args.object_name, file_path)
        logging.info("Successfully Downloaded " + args.object_name + " from " + args.bucket_name + " S3 bucket")
    except ClientError as e:
        logging.error(e)
        return False
    return True
