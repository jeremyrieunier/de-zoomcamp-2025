import pandas as pd
from sqlalchemy import create_engine
from time import time

# Create database connection
print("Connecting to database")
engine = create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')

try:
    print("Starting green taxi trips data ingestion")
    # Read CSV in chunks to handle large files efficiently using an iterator object
    df_iter = pd.read_csv('data_sources/green_tripdata_2019-10.csv.gz', iterator=True, chunksize=100000)

    # Iterate through chunks
    for i, chunk in enumerate(df_iter):
        t_start = time()

        # Convert datetime columns
        chunk['lpep_pickup_datetime'] = pd.to_datetime(chunk['lpep_pickup_datetime'])
        chunk['lpep_dropoff_datetime'] = pd.to_datetime(chunk['lpep_dropoff_datetime'])

        # Convert all column names to lowercase
        chunk.columns = chunk.columns.str.lower()

        # Insert chunk into the database
        chunk.to_sql(name="green_taxi_trips_2019_10", con=engine, if_exists='append',index=False)
        
        # Record end time and calculate duration
        t_end = time()
        print(f"Inserted chunk {i+1}, it took {(t_end - t_start):.3f} seconds")

# Catch and print any errors that occur
except Exception as e:
    print(f"Error occurred during green taxi trips ingestion: {e}")

try:
    print("Starting taxi zone lookup data ingestion")
    df = pd.read_csv('data_sources/taxi_zone_lookup.csv')
    df.columns = df.columns.str.lower()
    df.to_sql(name="taxi_zone_lookup", con=engine, if_exists="append", index=False)

    t_end = time()
    print(f"Inserted taxi zone lookup data in {(t_end - t_start):.3f} seconds")

# Catch and print any errors that occur
except Exception as e:
    print(f"Error occurred during taxi zone lookup ingestion: {e}")

        