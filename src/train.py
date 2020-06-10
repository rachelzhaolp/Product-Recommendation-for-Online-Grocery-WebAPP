import logging
import pandas as pd
from os import path
import config.config as conf
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from src.helper import read_csv, save_csv, load_config
import numpy as np

pd.options.mode.chained_assignment = None

logger = logging.getLogger(__name__)
project_path = path.dirname(path.dirname(path.abspath(__file__)))


def main(args):
    """
    main function to run the market basket analysis and save the recommendations to csv
    :param args: (argparse) user-input configuration file
    """
    try:
        config_path = project_path + "/" + args.config
        input_data_path = project_path + "/" + args.input
        output_data_path = project_path + "/" + args.output
        product_path = project_path + "/" + conf.PRODUCT_DIM

        config = load_config(config_path)
        df = read_csv(input_data_path)
        product = read_csv(product_path)

        result = train(df, **config['train'])

        # Join product object table to get the name and price.

        final_results = join_info(result, product, "StockCode", "StockCode")
        final_results = join_info(final_results, product, "rec1", "StockCode")
        final_results = join_info(final_results, product, "rec2", "StockCode")

        # format conf
        final_results['conf1'] = round(final_results['conf1'] * 100, 2)
        final_results['conf2'] = round(final_results['conf2'] * 100, 2)

        final_results = final_results[config["result_columns"]]

        # Write to output file
        save_csv(final_results, output_data_path)
    except KeyError as e3:
        logger.error("KeyError: " + str(e3))
    except ValueError as e4:
        logger.error("ValueError: " + str(e4) + " Please validate Values in the configuration file.")
    except Exception as e:
        logger.error("Unexpected error occurred when making recommendations: " + str(e))


def train(df, apriori_args, association_rules_args, ante_num_filter, rank_arg, rank_filter, to_columns):
    """
    Run market basket analysis on baskets data, return recommendations
    Args:
        df: (DataFrame) Baskets
        apriori_args: (Dictionary) Arguments of apriori()
        association_rules_args: (Dictionary) Arguments of the association_rules()
        ante_num_filter: (Integer) Threshold of the maximum number of items in antecedents
        rank_filter: (Integer) Threshold of number recommendations for each item
        rank_arg: (Dictionary) Argument of the rank() function
        to_columns: (List of String) Column names of the new DataFrame

    Returns: (DataFrame) Recommendations

    """

    df = df.set_index('Invoice')
    # all products
    prods = df.columns.to_frame()

    # Calculate support for different baskets
    frequent_itemsets = get_support(df, apriori_args)
    popular_list = get_popular(frequent_itemsets)

    # Calculate confidence
    rules = get_recommendations(frequent_itemsets, association_rules_args, ante_num_filter, rank_filter, rank_arg)

    # Change data types of antecedents and consequents to string
    rules = frozenset2String(rules, 'antecedents')
    rules = frozenset2String(rules, 'consequents')

    # Pivot the DataFrame
    rec = pivot_rules(rules, to_columns)
    # Get full table
    rec = get_full_table(prods, rec, to_columns)

    # Fill na
    rec = fill_no_rec(rec, popular_list)
    logger.info("Successfully made recommendations for {} products".format(len(rec)))
    return rec


def get_support(df, apriori_args):
    """
    Calculate support for each basket using apriori()
    Args:
        df: (DataFrame) Baskets
        apriori_args: (Dictionary) Arguments of apriori()

    Returns: (DataFrame)frequent_itemsets

    """
    logger.warning("Calculate supports for item sets is heavy on memory, please increase the memory limitation to at "
                   "least 12GB")
    logger.info("Calculating supports for the item sets")
    frequent_itemsets = apriori(df, **apriori_args)
    logger.info("Successfully calculated supports")
    if len(frequent_itemsets) < 2:
        raise ValueError("No items set meet the limit of minimum support, please use a smaller min_support.")
    else:
        return frequent_itemsets


def get_popular(frequent_itemsets):
    """
    Get the top 2 most items with highest support
    Args:
        frequent_itemsets: (DataFrame) frequent_itemsets, return of apriori()

    Returns: (List) top2 most frequent products

    """
    popularity = frequent_itemsets.sort_values(by=['support'], ascending=False).reset_index()['itemsets']
    most_popular = list(popularity[0])[0]
    second_popular = list(popularity[1])[0]
    return [most_popular, second_popular]


def get_recommendations(frequent_itemsets, association_rules_args, ante_num_filter, rank_filter, rank_arg):
    """
    Calculate confidence with association_rules
    Args:
        frequent_itemsets: (DataFrame) frequent_itemsets, return of apriori()
        association_rules_args: (Dictionary) Arguments of the association_rules()
        ante_num_filter: (Integer) Threshold of the maximum number of items in antecedents
        rank_filter: (Integer) Threshold of number recommendations for each item
        rank_arg: (Dictionary) Argument of the rank() function

    Returns:(DataFrame) association_rules

    """
    logger.info("Calculating confidence for association_rules")
    rules = association_rules(frequent_itemsets, **association_rules_args)
    if len(rules) == 0:
        raise ValueError("No rules meet the limit, please try a smaller min_support in get_support() or a samller "
                         "min_threshold ")
    else:
        # filter recommendations
        rules['ante_num'] = rules['antecedents'].apply(len)
        rules = rules[rules['ante_num'] <= ante_num_filter]
        rules.loc[:, 'rank'] = rules.groupby('antecedents')['confidence'].rank(**rank_arg)
        rules = rules[rules['rank'] <= rank_filter]
        logger.info("Successfully calculated confidences")
        return rules


def frozenset2String(rules, colname):
    """
    Change datatype of a given column from frozenset to String
    Args:
        rules: (DataFrame) Association rules
        colname: (String) Name of the column

    Returns:(DataFrame)

    """
    rules.loc[:, colname] = [','.join(map(str, prod)) for prod in rules[colname]]
    return rules


def pivot_rules(rules, to_columns):
    """
    Pivot the DataFrame of the association rules
    Args:
        rules: (DataFrame) Association rules
        to_columns: (List of String) Column names of the new DataFrame

    Returns:(DataFrame)

    """
    rec = rules.pivot(index='antecedents', columns='rank', values=['consequents', 'confidence'])
    if rec.shape[1] == 2:
        rec['rec2'] = np.nan
        rec['conf2'] = np.nan
        rec.columns = ['rec1', 'conf1', 'rec2', 'conf2']
    else:
        rec.columns = to_columns[1:]
    rec = rec.reset_index()
    return rec


def get_full_table(prods, rec, to_columns):
    """
    Left join product list with association rules, get full table
    Args:
        prods: (DataFrame) All products
        rec: (DataFrame) Recommendations
        to_columns: (List of String) Column names of the new DataFrame

    Returns:(DataFrame)

    """
    rec = prods.join(rec.set_index("antecedents"), how="left").reset_index()
    rec = rec.rename(columns={'index': 'StockCode'})
    rec = rec[to_columns]
    return rec


def fill_no_rec(rec, popular_list):
    """
    Fill NA in the full table
    Args:
        rec: (DataFrame) Recommendations
        popular_list: (List) top2 most frequent products

    Returns:(DataFrame)

    """
    rec['rec1'] = rec['rec1'].fillna(popular_list[0])
    rec['conf1'] = rec['conf1'].fillna(0)
    rec.loc[rec['rec1'] == popular_list[0], 'rec2'] = rec.loc[rec['rec1'] == popular_list[0], 'rec2'].fillna(
        popular_list[1])
    rec.loc[rec['rec1'] != popular_list[0], 'rec2'] = rec.loc[rec['rec1'] != popular_list[0], 'rec2'].fillna(
        popular_list[0])
    rec['conf2'] = rec['conf2'].fillna(0)
    return rec


def join_info(df, info_df, lefton, righton):
    """
    Join two tables
    Args:
        df: (DataFrame)
        info_df: (DataFrame)
        lefton: (String) Join key- left
        righton: (String) Join key- right

    Returns:(DataFrame)

    """
    to_df = df.set_index(lefton).join(info_df.set_index(righton), lsuffix='', rsuffix='_' + lefton,
                                      how="inner").reset_index()
    to_df = to_df.rename(columns={'index': lefton})
    return to_df
