from os import path
PROJECT_HOME = path.dirname(path.abspath(__file__))


"""
config for default path arguments in run.py
"""
# config
CONFIG_YAML = "config/config.yaml"
REPRODUCIBILITY_YAML = "config/reproducibility_test.yaml"
TEST_YAML = "config/test_units.yaml"

# raw data
RAW_DATA = "data/online_retail_II.csv"
OBJECT_NAME = "online_retail_II.csv"
BUCKET_NAME = "msia423-product-recommendation"

# clean data
CLEAN_DATA = "data/clean_data.csv"

# basket
BASKETS = "data/basket.csv"

# product_dim
PRODUCT_DIM = "data/product_dim.csv"

# train/test
TRAIN_DATA = "models/training_data.csv"
TEST_DATA = "models/test_data.csv"

# recommendations
REC_PATH = "models/rec.csv"

# evaluation
AUC_ACCURACY_PATH = "models/accuracy.csv"

# table to write rec into
TABLE = "prods_recs"
