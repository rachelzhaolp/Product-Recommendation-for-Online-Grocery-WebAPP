import logging
from os import path
import numpy as np
from src.helper import read_csv, save_csv, load_config

logger = logging.getLogger(__name__)
project_path = path.dirname(path.dirname(path.abspath(__file__)))


def main(args):
    """
    main function to create object table for products form the cleaned transactions
    :param args: (argparse) user-input configuration file
    """
    try:
        config_path = project_path + "/" + args.config
        input_data_path = project_path + "/" + args.input
        output_data_path = project_path + "/" + args.output

        config = load_config(config_path)
        df = read_csv(input_data_path)
        product = product_dim(df, **config['product_dim'])

        # Write to output file
        save_csv(product, output_data_path)
    except Exception as e:
        logger.error("Unexpected error occurred when creating object table for products: " + str(e))


def product_dim(df, to_columns):
    """
    Create object table for products form the cleaned transactions
    Args:
        df: (DataFrame) Cleaned data
        to_columns: (List) List of column names

    Returns: (DataFrame) Object table for the products

    """

    product = df.groupby(['StockCode', 'Category', 'Description']).apply(
        lambda x: round(np.average(x['Price'], weights=x['Quantity']), 2)).to_frame().reset_index()
    product.columns = to_columns

    return product

