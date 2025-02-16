import dlt

# Initialize a dlt pipeline connecting to a DuckDB database
pipeline = dlt.pipeline(
    pipeline_name = "ny_taxi_pipeline",
    destination="duckdb"
)

# Load the rides table into a pandas dataFrame and count records 
df = pipeline.dataset(dataset_type="default").rides.df()

print(f"Total number of records: {len(df)}")

# Open a SQL client connection to execute the query
with pipeline.sql_client() as client:
    res = client.execute_sql(
        """
        SELECT
        AVG(date_diff('minute', trip_pickup_date_time, trip_dropoff_date_time))
        FROM rides;
        """
    )
    print(f"The average trip duration is {res[0][0]}")

