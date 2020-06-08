import logging
from os import path
from src.helper import read_csv, save_csv, load_config

logger = logging.getLogger(__name__)
project_path = path.dirname(path.dirname(path.abspath(__file__)))


def create_basket(df, product_num, rank_arg):
    """
    Create basket from cleaned data for market basket analysis
    Args:
        df: DataFrame
        product_num: (Integer) keep the top `product_num` most frequent products
        rank_arg: (Dict) Arguments for the rank() function

    Returns:DataFrame

    """

    try:
        # filter product_num most frequently products
        cnt = df.groupby('StockCode').count()
        cnt['rank'] = cnt['Invoice'].rank(**rank_arg)
        s_code = list(cnt[cnt['rank'] <= product_num].index)
        filtered_df = df[df['StockCode'].isin(s_code)]

        # create baskets
        basket = (filtered_df.groupby(['Invoice', 'StockCode'])['Quantity']
                  .sum().unstack().reset_index().fillna(0)
                  .set_index('Invoice'))
        # one hot encoding
        basket[basket > 0] = 1

        return basket

    except KeyError as e1:
        logger.error("KeyError: " + str(e1) + " Please validate Keys in the configuration file.")
        raise KeyError("Input data does not have all required columns.")
    except ValueError as e2:
        logger.error("ValueError: " + str(e2) + " Please validate Values in the configuration file.")
        raise ValueError
    except Exception as e:
        logger.error("Unexpected error occurred when creating basket: " + str(e))


def main(args):
    """
    main function to clean data
    :param args: (argparse) user-input configuration file
    """
    try:
        config_path = project_path + "/" + args.config
        input_data_path = project_path + "/" + args.input
        output_data_path = project_path + "/" + args.output

        config = load_config(config_path)
        df = read_csv(input_data_path)
        basket = create_basket(df, **config['create_basket'])

        # Write to output file
        save_csv(basket, output_data_path, index=True)
    except Exception as e:
        logger.error("Unexpected error occurred when creating basket: " + str(e))
