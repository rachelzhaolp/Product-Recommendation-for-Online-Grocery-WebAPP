# Product Recommendation - Project Repository
  

<!-- toc -->
#### Developer: Luping(Rachel) Zhao
#### QA: Siqi Li

<!-- toc -->


- [Project Charter](#Project-Charter)
- [Backlog](#Backlog)
- [Directory Structure](#directory-structure)
- [Build the Data Pipeline](#How to build the data pipeline )
<!-- 
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)
-->
 
<!-- tocstop -->

## Project Charter
**Vision**: Retailers can never assume that the customers know all of their offerings. But rather, they must make efforts to present all applicable options in ways that improve customer experience and increase sales.  While brick-and-mortar shops guild customers' shopping experience with salespeople, online retailers need to find their way to give specific product recommendations.

**Mission**: The app will prompt users to select an initial product into the cart and then recommend the products frequently bought together. This project uses the [Online Retail II UCI](https://www.kaggle.com/mashlyn/online-retail-ii-uci) data set compiled by Mashlyn on Kaggle.com, which contains all the transactions occurring for a UK-based online retail between 01/12/2009 and 09/12/2011. The model will find frequent patterns in this transaction database using Market Basket Analysis, the most common association rule mining approach used by large retailers like Amazon.

**Success criteria**:
- Business outcome metrics: 15% increase in sales and a 5% increase in daily active users compared with no recommendations.
- Model performance metric: define the absolute threshold of the Decision-support metrics(Accuracy, recall, precision) and Rank Metrics(mRR, mAP, DCG) to evaluate a recommender model is tricky, however, we use the following value for now.
1. 55% cross-validated f-score
2. 45% Mean Average Precision


## Backlog
**Main Initiative**:
Increase the sales of online retailers by deploying market basket analysis to give product recommendations using market basket analysis.

**Initiative 1: Model Development**
1. Epic 1: Data Acquisition and Ingestion
    *	Story 1: Data Acquisition: download data from Kaggle (0 point)
    * Story 2: Understand the meaning of each variable (0 point)
    * Story 3: Exploratory Data Analysis (1 point)
    * Story 4: Data cleaning with outliers, missing values, skewness, imbalance; Romove products with too few records to make a recommendation(2 point)
    
2. Epic 2: Develop the Market Busket Analysis  model
    *	Story 1: Split data into training and validation sets (0 point)
    * Story 2: Build the market busket analysis model(4 points)
    * Story 3: Evaluate model with cross-validated decision-support metrics(Accuracy, recall, precision) and cross-validated rank metrics(mRR, mAP, DCG) (2 points)


**Initiative 2: Product Development**
1. Epic 1: Build data pipeline (8 points)
    * Story 1: Create S3 bucket and load raw data (2 points)
    * Story 2: Set up RDS instance and create suitable Database schema (i.e. tables) (2 points)
    * Story 3: Enable the model to access data from S3 bucket, and return the predictions to RDS (2 points)
2. Epic 2: Web app design: (4 points)
    *	Story 1: User interface design (2 points)
    *	Story 2: User interaction design (2 points)
3. Epic 3: Web app (Flask) Development (8 points -- needs to be broken down more when it comes to execution)
    * Story 1: Set up the web server with Flask
    * Story 2: Achieve the desired functionality
    
**Initiative 3: Quality Assurance**
1. Epic 1: Write Documentations and comments (4 points)
    *	Story 1: Compile README.md to clarify the desired functionality and how to run the app (2 points)
    *	Story 2: Ensure code readability (1 points)
2. Epic 2:Testing (4 points)
    *	Story 1: Testing the functionality of the app and the reproducibility of the model(2 points)
    *	Story 2: Validate the efficiency of the design(2 points)
    *	Story 3: Debug/refine if needed (-)
3. Epic 3: Final roll-out (2 points)
    


**Icebox**:

**Initiative 3: Product Development**
2. Epic 2: Web app design
3. Epic 3: Web app (Flask) Development


<!-- tocstop -->
## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## How to build the data pipeline 
The online retail product recommendation app applies an offline training method, which requires the developer to transform data between local and S3 buckets, and then store the prediction into RDS. Follow the instructions in this section one should be able to build the data pipeline. The dataset of this project has been downloaded form [Kaggle](https://www.kaggle.com/mashlyn/online-retail-ii-uci) and stored under `data/`.

### Step 0: Clone the repository to your computer and change the working directory into the repository
```bash
# clone with ssh, the repository will be download to your current working directory. 
git clone git@github.com:rachelzhaolp/2020-msia423-Zhao-Luping.git
# change working directory to the repository
cd 2020-msia423-Zhao-Luping
```

### Step 1: Update the `.env` file. Replace the pseudo value with your credentials 
1. Open vim in bash with `vi config/.env`, press i into the edit mode 
```bash 
vi config/.env
```
Update the following credentials, press ESC, then input `:wq` to save the changes. 
* `AWS_ACCESS_KEY_ID` 
* `AWS_SECRET_ACCESS_KEY`
* `MYSQL_USER`
* `MYSQL_PASSWORD`

### Step 2: Build docker image and tag it with `msia423`, msia423 is the name of the image
 ```bash
 docker build -f app/Dockerfile -t msia423 .
 ```
By default, the docker build command will look for a Dockerfile at the root of the build context. The -f, —file, the option lets you specify the path to an alternative file to use instead. Our Dockerfile is under `app/`.

### Step 3: Upload rawdata into S3 bucket
```
docker run --env-file=config/.env msia423 run.py upload_file
```
The `upload_file()` function is defined in `interact_s3.py` under `src/`, it takes three argument: `file_name`, `bucket_name`, `object_name`. You can find their description in the python script. By default, this function will upload the `online_retail_II.csv` file in the `data/` directory to S3 bucket `msia423-product-recommendation` and name the new object `online_retail_II.csv`. If you intend to upload other files, please put the file in the `data/` directory and change `FILE_NAME` in the `config.py`.

To download files from S3 bucket, run:
```bash
docker run --env-file=config/.env msia423 run.py download_file. 
```
`download_file()` has the same arguments as `upload_file()`, the downloaded file will be stored in `data/`

### Step 4: Create new table in RDS
```
docker run --env-file=config/.env msia423 run.py create_db --rds=True
```
Set `rds` to `True` will create a new database with a table named prds_rec in RDS. 
By default, `rds` equals to False, and the database will be created on your local machine. Under `data/`.
```
docker run --env-file=config/.env msia423 run.py create_db
```
