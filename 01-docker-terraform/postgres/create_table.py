from sqlalchemy import create_engine, text

# Create database connection
print("Connecting to database")
engine = create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')

# Drop table if exists
drop_table = "DROP TABLE IF EXISTS green_taxi_trips_2019_10;"

# SQL statement to create table
create_table = """
CREATE TABLE IF NOT EXISTS green_taxi_trips_2019_10 (
    VendorID INT,
    lpep_pickup_datetime TIMESTAMP,
    lpep_dropoff_datetime TIMESTAMP,
    store_and_fwd_flag VARCHAR(1),
    RatecodeID INT,
    PULocationID INT,
    DOLocationID INT,
    passenger_count INT,
    trip_distance DECIMAL(10,2),
    fare_amount DECIMAL(10,2),
    extra DECIMAL(10,2),
    mta_tax DECIMAL(10,2),
    tip_amount DECIMAL(10,2),
    tolls_amount INT,
    ehail_fee DECIMAL(10,2),
    improvement_surcharge DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    payment_type INT,
    trip_type INT,
    congestion_surcharge INT
);
"""

try:
    # Create a connection and execute SQL
    with engine.connect() as conn:
        print("Dropping table if exists...")
        conn.execute(text(drop_table)) # Execute the DROP TABLE statement

        print("Creating table green_taxi_trips_2019_10")
        conn.execute(text(create_table)) # Execute the CREATE TABLE statement
        conn.commit()
        print("Table created")

# Catch and print any errors that occur
except Exception as e:
    print(f"Error occurred: {e}")

