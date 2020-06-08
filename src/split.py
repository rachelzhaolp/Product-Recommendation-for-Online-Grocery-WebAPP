import logging
from os import path
from sklearn import model_selection
from src.helper import read_csv, save_csv, load_config

logger = logging.getLogger(__name__)
project_path = path.dirname(path.dirname(path.abspath(__file__)))


def split(df, split_data):
    """
    Split and store the training/test data
    :param df: (String) Relative local file path of the data source
    :param split_data: (Dictionary) Arguments to split the data into training and test
    :return: None
    """
    try:
        # Split data into test and train
        df_train, df_test = model_selection.train_test_split(df, **split_data)

        return [df_train, df_test]

    except ValueError as e1:
        logger.error("ValueError: " + str(e1) + " Please validate Values in the configuration file.")
    except Exception as e:
        logger.error("Unexpected error occurred when splitting data: " + str(e))


def main(args):
    """
    main function to split data
    :param args: (argparse) user-input configuration file
    """
    try:

        config_path = project_path + "/" + args.config
        input_data_path = project_path + "/" + args.input
        out_train_path = project_path + "/" + args.output_train
        out_test_path = project_path + "/" + args.output_test

        config = load_config(config_path)
        df = read_csv(input_data_path)
        df_train, df_test = split(df, **config['split_data'])

        # Write to output file
        save_csv(df_train, out_train_path)
        save_csv(df_test, out_test_path)

    except Exception as e:
        logger.error("Unexpected error occurred when splitting data: " + str(e))
