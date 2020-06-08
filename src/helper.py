import logging
from os import path
import pandas as pd
import yaml

logger = logging.getLogger(__name__)
project_path = path.dirname(path.dirname(path.abspath(__file__)))


def read_csv(input_data_path):
    try:
        # Load data from local file
        logger.info("Trying to load data from %s", input_data_path)
        df = pd.read_csv(input_data_path, header=0, low_memory=False)
        logger.info("Successfully loaded data from {}".format(input_data_path))
        return df
    except FileNotFoundError as e1:
        logger.error('FileNotFoundError: {}'.format(e1))


def save_csv(df, output_data_path, index=False):
    try:
        # Save data to file
        df.to_csv(output_data_path, index=index)
        logger.info("Successfully saved data to {}".format(output_data_path))
    except FileNotFoundError as e1:
        logger.error('FileNotFoundError: {}'.format(e1))


def load_config(config_path):
    try:
        with open(config_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        logger.info("Configuration file loaded from %s" % config_path)
        return config
    except FileNotFoundError as e1:
        logger.error('FileNotFoundError: {}'.format(e1))


def check_num(from_df, to_df):
    from_num = len(from_df)
    to_num = len(to_df)
    return [from_num - to_num, to_num]
