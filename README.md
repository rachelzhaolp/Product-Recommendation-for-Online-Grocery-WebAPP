# Product Recommendation - Project Repository
  

<!-- toc -->
#### Developer: Luping(Rachel) Zhao
#### QA: Siqi Li

<!-- toc -->


- [Project Charter](#Project-Charter)
- [Backlog](#Backlog)
- [Directory structure](#directory-structure)
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

## Running the app
### 1. Initialize the database 

#### Create the database with a single song 
To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create_db --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py create_db` creates a database at `sqlite:///data/tracks.db` with the initial song *Radar* by Britney spears. 
#### Adding additional songs 
To add an additional song:

`python run.py ingest --engine_string=<engine_string> --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

By default, `python run.py ingest` adds *Minor Cause* by Emancipator to the SQLite database located in `sqlite:///data/tracks.db`.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). We will cover SQLAlchemy and connection strings in the SQLAlchemy lab session on 
##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/tracks.db'

```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://///Users/cmawer/Repos/2020-MSIA423-template-repository/data/tracks.db'
```


### 2. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in app/Dockerfile 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "penny-lane"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 3. Run the Flask app 

To run the Flask app, run: 

```bash
python app.py
```

You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

## Running the app in Docker 

### 1. Build the image 

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run from this directory (the root of the repo): 

```bash
 docker build -f app/Dockerfile -t pennylane .
```

This command builds the Docker image, with the tag `pennylane`, based on the instructions in `app/Dockerfile` and the files existing in this directory.
 
### 2. Run the container 

To run the app, run from this directory: 

```bash
docker run -p 5000:5000 --name test pennylane
```
You should now be able to access the app at http://0.0.0.0:5000/ in your browser.

This command runs the `pennylane` image as a container named `test` and forwards the port 5000 from container to your laptop so that you can access the flask app exposed through that port. 

If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `app/Dockerfile`)

### 3. Kill the container 

Once finished with the app, you will need to kill the container. To do so: 

```bash
docker kill test 
```

where `test` is the name given in the `docker run` command.
