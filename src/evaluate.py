import logging
import pandas as pd
from os import path
from src.helper import read_csv, save_csv

logger = logging.getLogger(__name__)
project_path = path.dirname(path.dirname(path.abspath(__file__)))


def main(args):
    """
    main function to clean data
    :param args: (argparse) user-input configuration file
    """
    try:
        rec_path = project_path + "/" + args.rec
        test_data_path = project_path + "/" + args.test
        output_data_path = project_path + "/" + args.output

        rec = read_csv(rec_path)
        test = read_csv(test_data_path)

        accuracy = accuracy_calculator(rec, test)
        # Write to output file
        save_csv(accuracy, output_data_path)
    except Exception as e:
        logger.error("Unexpected error occurred when evaluation: " + str(e))


def accuracy_calculator(rec, test):
    """
    Calculate recommendation accuracy
    Args:
        rec: (DataFrame) Recommendations
        test: (DataFrame) Test baskets

    Returns:

    """
    out = pd.DataFrame(columns=['StockCode', 'rec1', 'rec2', 'num_stock', 'num_with_rec1', 'num_with_rec2'])
    for index, row in rec.iterrows():
        StockCode = row["StockCode"]
        rec1 = row["rec1"]
        rec2 = row["rec2"]
        num_stock = test[test[StockCode] == 1].shape[0]
        num_with_rec1 = test[(test[StockCode] == 1) & (test[rec1] == 1)].shape[0]
        num_with_rec2 = test[(test[StockCode] == 1) & (test[rec2] == 1)].shape[0]
        temp = pd.DataFrame(data=[[StockCode, rec1, rec2, num_stock, num_with_rec1, num_with_rec2]],
                            columns=['StockCode', 'rec1', 'rec2', 'num_stock', 'num_with_rec1', 'num_with_rec2'])
        out = pd.concat([out, temp])
    out['rec1_accuracy'] = out['num_with_rec1'] / out['num_stock']
    out['rec2_accuracy'] = out['num_with_rec2'] / out['num_stock']
    out['overall_accuracy'] = (out['rec1_accuracy'] + out['rec2_accuracy']) / 2
    return out[['rec1_accuracy', 'rec2_accuracy', 'overall_accuracy']].agg(['mean', 'max']).round(2)
