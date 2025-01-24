from sqlalchemy import create_engine, text

# Create database connection
print("Connecting to database")
engine = create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')

# # Drop table if exists
drop_taxi_trips = "DROP TABLE IF EXISTS green_taxi_trips_2019_10;"
drop_taxi_zone = "DROP TABLE IF EXISTS taxi_zone_lookup;"

# SQL statement to create taxi trips table
create_table_taxi_trips = """
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

# SQL statement to create taxi zone table
create_table_taxi_zone = """
CREATE TABLE IF NOT EXISTS taxi_zone_lookup (
    LocationID INT,
    Borough TEXT,
    Zone TEXT,
    service_zone TEXT
);
"""

try:
    # Create a connection and execute SQL
    with engine.connect() as conn:
        print("Dropping table if exists")
        conn.execute(text(drop_taxi_trips)) # Execute the DROP TABLE statement
        conn.execute(text(drop_taxi_zone)) # Execute the DROP TABLE statement

        print("Creating table green_taxi_trips_2019_10")
        conn.execute(text(create_table_taxi_trips)) # Execute the CREATE TABLE statement

        print("Creating table taxi_zone_lookup")
        conn.execute(text(create_table_taxi_zone)) # Execute the CREATE TABLE statement

        conn.commit()
        print("All tables created successfully")

# Catch and print any errors that occur
except Exception as e:
    print(f"Error occurred: {e}")
