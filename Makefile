DATA_PATH=data/
CONFIG_PATH=config/
MODEL_PATH=model/
FIGURE_PATH=figures/
EVALUATION_PATH=evaluations/
TEST_PATH=test/

## acquire
${DATA_PATH}online_retail_II.csv:
	python3 run.py acquire

acquire: ${DATA_PATH}online_retail_II.csv ${CONFIG_PATH}config.yaml

## clean_data
${DATA_PATH}clean_data.csv: ${DATA_PATH}online_retail_II.csv ${CONFIG_PATH}config.yaml
	python3 run.py clean

clean_data: ${DATA_PATH}clean_data.csv

## product_dim
${DATA_PATH}product_dim.csv: ${DATA_PATH}clean_data.csv ${CONFIG_PATH}config.yaml
	python3 run.py product_dim

product_dim: ${DATA_PATH}product_dim.csv

## create_basket
${DATA_PATH}basket.csv: ${DATA_PATH}clean_data.csv ${CONFIG_PATH}config.yaml
	python3 run.py create_basket

create_basket: ${DATA_PATH}basket.csv

# split data into training and test csv
split: ${DATA_PATH}basket.csv ${CONFIG_PATH}config.yaml
	python3 run.py split

${DATA_PATH}training_data.csv: split
${DATA_PATH}test_data.csv: split

## make recommendations
${DATA_PATH}rec.csv: ${DATA_PATH}training_data.csv ${DATA_PATH}product_dim.csv ${CONFIG_PATH}config.yaml
	python3 run.py train

train: ${DATA_PATH}rec.csv

## evaluation
${EVALUATION_PATH}auc_accuracy.csv: ${DATA_PATH}test_data.csv ${DATA_PATH}rec.csv
	python3 run.py evaluate

evaluate: ${EVALUATION_PATH}auc_accuracy.csv


tests:
	py.test

reproducibility_tests:
	python3 run.py reproducibility_tests


clean:
	rm -f data/*
	rm -f models/*
	rm -f figures/*
	rm -f evaluations/*


all: acquire clean_data product_dim create_basket split train evaluate

.PHONY: tests reproducibility_tests clean all acquire clean_data product_dim create_basket split train evaluate

