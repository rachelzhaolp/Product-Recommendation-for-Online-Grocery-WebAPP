import logging
from os import path
import boto3
import botocore
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)
project_path = path.dirname(path.dirname(path.abspath(__file__)))


def acquire(object_name, bucket_name, output):
    """

    Args:
        object_name: (String) Name of the object to download
        bucket_name: (String) S3 bucket to download from
        output: (String) path of the downloaded file

    Returns: None

    """

    data_path = project_path + "/" + output
    s3 = boto3.resource('s3')
    try:

        logger.info("Acquiring {} from {}".format(object_name, bucket_name))
        s3.Bucket(bucket_name).download_file(object_name, data_path)
        logging.info("Successfully downloaded data to {}".format(data_path))

    except botocore.exceptions.ClientError as e1:
        logger.error("ClientError: " + str(e1))
        raise botocore.exceptions.ClientError
    except botocore.exceptions.NoCredentialsError as e3:
        logger.error("NoCredentialsError: " + str(e3))
        raise botocore.exceptions.NoCredentialsError
    except Exception as e2:
        logger.error("Unexpected error occurred when acquiring data: " + str(e2))


def main(args):
    """
    main function to Acquire data
    :param args: (argparse) user-input configuration file
    """

    try:
        var = vars(args)
        var.pop('func', None)
        acquire(**var)
    except Exception as e2:
        logger.error("Unexpected error occurred when acquiring data: " + str(e2))
