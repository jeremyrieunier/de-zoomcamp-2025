# Workshop Data Ingestion with dlt: Homework

Dataset & API
I've used NYC Taxi data using this API endpoint
```
https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api
```
- Data format: Paginated JSON (1,000 records per page)
- API Pagination: Stop when an empty page is returned

## Question 1: dlt Version
I ran the following command to check the version:
`dlt --version`

Output is `dlt 1.6.1`

## Question 2: How many tables were created?
- 2
- **4**
- 6
- 8

Output of the script [nyc_taxi_pipeline.py](nyc_taxi_pipeline.py) returns the following
```
Tables in database:
                  name
0           _dlt_loads
1  _dlt_pipeline_state
2         _dlt_version
3                rides
```

## Question 3: What is the total number of records extracted?
- 2500
- 5000
- 7500
- **10000**

Output of the script [nyc_taxi_explore.py](nyc_taxi_explore.py) returns the following
```
Total number of records: 10000
```

## Question 4: What is the average trip duration?
- **12.3049**
- 22.3049
- 32.3049
- 42.3049

Output of the script [nyc_taxi_explore.py](nyc_taxi_explore.py) returns the following
```
The average trip duration is 12.3049
```