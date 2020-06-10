import logging.config
from os import path
import boto3
from botocore.exceptions import ClientError

import config.config as config

logger = logging.getLogger(__name__)
project_path = path.dirname(path.dirname(path.abspath(__file__)))


def upload_file(args):
    """Upload a file to an S3 bucket

    Args:
        args: argparse args - should include args.file_name, args.bucket_name, args.object_name
        args.file_name: String, file to upload
        args.bucket_name: String, S3 bucket to upload into
        args.object_name: String, object name of the uploaded file
    """

    data_path = project_path + "/" + args.file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(data_path, args.bucket_name, args.object_name)
        logging.info("Successfully uploaded " + args.file_name + " to " + args.bucket_name + " S3 bucket")
    except ClientError as e:
        logging.error(e)
    except FileNotFoundError as e2:
        logger.error('FileNotFoundError: {}'.format(e2))
    except Exception as e3:
        logger.error("Unexpected error occurred when uploading file to S3: " + str(e3))


