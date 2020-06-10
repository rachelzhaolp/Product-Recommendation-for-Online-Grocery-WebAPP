DATA_PATH=data/
CONFIG_PATH=config/
MODEL_PATH=models/

## acquire
${DATA_PATH}online_retail_II.csv:
	python3 run.py acquire --output=${DATA_PATH}online_retail_II.csv

acquire: ${DATA_PATH}online_retail_II.csv

## clean_data
${DATA_PATH}clean_data.csv: ${DATA_PATH}online_retail_II.csv ${CONFIG_PATH}config.yaml
	python3 run.py clean_data  --input=${DATA_PATH}online_retail_II.csv --output=${DATA_PATH}clean_data.csv --config=${CONFIG_PATH}config.yaml
preprocess: ${DATA_PATH}/preprocessed.csv

clean_data: ${DATA_PATH}clean_data.csv

## product_dim
${DATA_PATH}product_dim.csv: ${DATA_PATH}clean_data.csv ${CONFIG_PATH}config.yaml
	python3 run.py product_dim --input=${DATA_PATH}clean_data.csv --output=${DATA_PATH}product_dim.csv --config=${CONFIG_PATH}config.yaml

product_dim: ${DATA_PATH}product_dim.csv

## create_basket
${DATA_PATH}basket.csv: ${DATA_PATH}clean_data.csv ${CONFIG_PATH}config.yaml
	python3 run.py create_basket --input=${DATA_PATH}clean_data.csv --output=${DATA_PATH}basket.csv --config=${CONFIG_PATH}config.yaml

create_basket: ${DATA_PATH}basket.csv

# split data into training and test csv
split: ${DATA_PATH}basket.csv ${CONFIG_PATH}config.yaml
	python3 run.py split --input=${DATA_PATH}basket.csv --output_train=${MODEL_PATH}training_data.csv --output_test=${MODEL_PATH}test_data.csv --config=${CONFIG_PATH}config.yaml

${MODEL_PATH}training_data.csv: split
${MODEL_PATH}test_data.csv: split

## make recommendations
${MODEL_PATH}rec.csv: ${MODEL_PATH}training_data.csv ${DATA_PATH}product_dim.csv ${CONFIG_PATH}config.yaml
	python3 run.py train --input=${MODEL_PATH}training_data.csv --output=${MODEL_PATH}rec.csv --config=${CONFIG_PATH}config.yaml

train: ${MODEL_PATH}rec.csv

## evaluation
${MODEL_PATH}auc_accuracy.csv: ${MODEL_PATH}test_data.csv ${MODEL_PATH}rec.csv
	python3 run.py evaluate --rec=${MODEL_PATH}rec.csv --test=${MODEL_PATH}test_data.csv --output=${MODEL_PATH}accuracy.csv

evaluate: ${MODEL_PATH}auc_accuracy.csv


tests:
	py.test

reproducibility_tests: all
	python3 run.py reproducibility_tests --config=${CONFIG_PATH}reproducibility_test.yaml

## create_database
add_rec: ${MODEL_PATH}rec.csv
	python3 run.py add_rec

evaluate: ${MODEL_PATH}auc_accuracy.csv

clean:
	rm -f ${DATA_PATH}*.csv
	rm -f ${MODEL_PATH}*


all: acquire clean_data product_dim create_basket split train evaluate

.PHONY: tests reproducibility_tests clean all acquire clean_data product_dim create_basket split train evaluate

