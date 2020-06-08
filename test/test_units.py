import pandas as pd
import yaml
from os import path
import pytest
from src.clean import clean, remove_na, remove_cancel, remove_invalid_prod, remove_return, remove_wrong, clean_desc
from src.product_dim import product_dim
from src.create_basket import create_basket
from src.train import train, get_support
from src.helper import read_csv
import numpy as np

# Get project path
project_path = path.dirname(path.dirname(path.abspath(__file__)))
test_config_path = project_path + "/test/test_units.yaml"
func_config_path = project_path + "/config/config.yaml"

# Load configurations from .yaml
with open(test_config_path, "r") as f:
    test_conf = yaml.load(f, Loader=yaml.FullLoader)
with open(func_config_path, "r") as f:
    func_conf = yaml.load(f, Loader=yaml.FullLoader)

# Unit test for clean
raw_data_path = project_path + "/" + test_conf['raw_data']
raw_df = read_csv(raw_data_path)


def test_clean_valid():
    """
    Test clean --happy path
    This function clean the raw data
    """
    true_data_path = project_path + "/" + test_conf['clean_data']
    true_df = pd.read_csv(true_data_path, dtype=str)

    test_df = clean(raw_df, **func_conf['clean'])
    test_df = test_df.astype(str)

    assert true_df.equals(test_df)


def test_clean_invalid():
    """
    Test clean --unhappy path
    """

    unhappy_df = raw_df.drop("StockCode", axis=1)

    with pytest.raises(KeyError):
        clean(unhappy_df, **func_conf['clean'])


def test_remove_na():
    """
    remove_na() removes rows from input DataFrame
    """
    test_df = remove_na(raw_df)
    assert test_df.isnull().sum().sum() == 0


def test_remove_cancel():
    """
    remove_cancel() removes rows whose Invoice contains 'C'
    """
    test_df = remove_cancel(raw_df)
    assert sum(test_df['Invoice'].str.contains("C")) == 0


def test_remove_invalid_prod():
    """
    remove_invalid_prod() removes rows with invalid StockCode
    """
    test_df = remove_invalid_prod(raw_df)
    assert len(test_df) == sum(test_df['StockCode'].str.match(r'\d{5}[A-Z]*'))


def test_remove_return():
    """
    remove_return() removes rows with negative quantity
    """
    test_df = remove_return(raw_df)
    assert sum(test_df['Quantity'] < 0) == 0


def test_remove_wrong():
    """
    remove_wrong() removes wrong transactions
    """
    test_df = remove_wrong(raw_df)
    assert sum(test_df['Price'] <= 0) == 0


def test_clean_desc():
    """
    clean_desc() makes all valid product has one and only one description
    """
    test_df = clean_desc(raw_df)
    assert max(test_df.groupby('StockCode')['Description_clean'].nunique()) == 1


# Unit test for create basket and product_dim

clean_data_path = project_path + "/" + test_conf['clean_data']
clean_df = read_csv(clean_data_path)


def test_create_basket_valid():
    """
    Test create_basket() --happy path
    """
    true_data_path = project_path + "/" + test_conf['basket_data']
    true_df = pd.read_csv(true_data_path, dtype=str)

    test_df = create_basket(clean_df, **func_conf['create_basket'])
    test_df = test_df.reset_index()
    test_df = test_df.astype(str)

    assert np.array_equal(true_df.values, test_df.values)


def test_create_basket_invalid():
    """
    Test create_basket() --unhappy path
    """

    unhappy_df = clean_df.drop("StockCode", axis=1)

    with pytest.raises(KeyError):
        create_basket(unhappy_df, **func_conf['create_basket'])


def test_product_dim_valid():
    """
    Test product_dim() --happy path
    """
    true_data_path = project_path + "/" + test_conf['product_dim']
    true_df = pd.read_csv(true_data_path, dtype=str)

    test_df = product_dim(clean_df, **func_conf['product_dim'])
    test_df = test_df.astype(str)

    assert true_df.equals(test_df)


def test_product_dim_invalid():
    """
    Test product_dim() --unhappy path
    """

    unhappy_df = clean_df.drop("StockCode", axis=1)

    with pytest.raises(KeyError):
        product_dim(unhappy_df, **func_conf['product_dim'])


# Unit test for train
training_path = project_path + "/" + test_conf['training_data']
training_data = read_csv(training_path)


def test_get_support_invalid():
    """
    Test product_dim() --unhappy path
    Wrong apriori_args value
    """
    with pytest.raises(ValueError):
        get_support(training_data, apriori_args=test_conf['wrong_apriori_args'])


def test_train_valid():
    """
    Test train() --happy path
    number of columns equals to product_num, one for each product. All products has two different recommendations
    """
    result = train(training_data, **func_conf['train'])

    assert len(result) == func_conf['create_basket']['product_num'] \
           and len(result['StockCode'].unique()) \
           and result.isnull().sum().sum() == 0
