import logging
from os import path

from src.helper import read_csv, save_csv, load_config, check_num

logger = logging.getLogger(__name__)
project_path = path.dirname(path.dirname(path.abspath(__file__)))


def main(args):
    """
    main function to load raw data, clean data and save leaned data to csv
    :param args: (argparse) user-input configuration file
    """
    try:
        config_path = project_path + "/" + args.config
        input_data_path = project_path + "/" + args.input
        output_data_path = project_path + "/" + args.output

        config = load_config(config_path)
        df = read_csv(input_data_path)
        clean_data = clean(df, **config['clean'])

        # Write to output file
        save_csv(clean_data, output_data_path)
    except KeyError as e3:
        logger.error("KeyError: " + str(e3))
    except Exception as e:
        logger.error("Unexpected error occurred when cleaning data: " + str(e))


def clean(df, columns_to_keep, to_columns):
    """
    Clean raw data
    Args:
        df: (DataFrame) DataFrame of raw data
        columns_to_keep: (String) Required columns
        to_columns: (String) Columns names of the output file

    Returns:DataFrame

    """

    # Keep only related columns before dropna()
    df = df[columns_to_keep]

    clean_data = remove_na(df)
    clean_data = remove_cancel(clean_data)
    clean_data = remove_invalid_prod(clean_data)
    clean_data = remove_return(clean_data)
    clean_data = remove_wrong(clean_data)
    clean_data = clean_desc(clean_data)
    clean_data.columns = to_columns

    return clean_data


def remove_na(from_df):
    """
    Remove rows contains na
    Args:
        from_df: DataFrame

    Returns:DataFrame

    """
    to_df = from_df.dropna()
    remove, remain = check_num(from_df, to_df)
    logger.debug("Removed {} rows contains NA, {} records remained".format(remove, remain))
    return to_df


def remove_cancel(from_df):
    """
    Remove cancelled orders
    Args:
        from_df: DataFrame

    Returns:DataFrame

    """
    from_df['Invoice'] = from_df['Invoice'].astype('str')
    to_df = from_df[~from_df['Invoice'].str.contains('C')]
    remove, remain = check_num(from_df, to_df)
    logger.debug("Removed {} cancelled orders, {} records remained".format(remove, remain))
    return to_df


def remove_invalid_prod(from_df):
    """
    Remove records with invalid product code
    Args:
        from_df: DataFrame

    Returns:DataFrame

    """
    to_df = from_df[from_df['StockCode'].str.match(r'\d{5}[A-Z]*')]
    to_df.loc[:, 'Category'] = to_df["StockCode"].str.replace(r"[^0-9]", "")
    remove, remain = check_num(from_df, to_df)
    logger.debug("Removed {} records with invalid StockCode, {} records remained".format(remove, remain))
    return to_df


def remove_return(from_df):
    """
    Remove return transactions
    Args:
        from_df: DataFrame

    Returns:DataFrame

    """
    to_df = from_df[from_df['Quantity'] >= 0]
    remove, remain = check_num(from_df, to_df)
    logger.debug("Removed {} return transactions, {} records remained".format(remove, remain))
    return to_df


def remove_wrong(from_df):
    """
    Remove wrong transactions
    Args:
        from_df: DataFrame

    Returns:DataFrame

    """
    to_df = from_df[from_df['Price'] > 0]
    remove, remain = check_num(from_df, to_df)
    logger.debug("Removed {} wrong transactions, {} records remained".format(remove, remain))
    return to_df


def clean_desc(from_df):
    """Clean product name, make sure each product only has one name

    Args:
        from_df: DataFrame

    Returns:DataFrame

    """
    from_df['Description'] = from_df['Description'].str.strip()
    # Get one and only one description for each product
    StockCode_cnt = from_df.groupby(['StockCode', 'Description']).count()
    StockCode_cnt['rank'] = StockCode_cnt.groupby(['StockCode'])['Invoice'].rank(method='first', ascending=False)
    StockCode_cnt = StockCode_cnt.reset_index()
    clean_desc = StockCode_cnt[StockCode_cnt['rank'] == 1][['StockCode', 'Description']]

    from_df = from_df.set_index('StockCode').join(clean_desc.set_index("StockCode"), lsuffix='_raw', rsuffix='_clean',
                                                  how="inner")
    to_df = from_df.drop('Description_raw', axis=1).reset_index()
    logger.debug("Successfully cleaned Description.")
    return to_df
