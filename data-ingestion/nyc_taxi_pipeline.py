import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator
import duckdb

# Define a data resource that will fetch NYC taxi ride data from an API
@dlt.resource(name="rides")  
def ny_taxi_rides():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator = PageNumberPaginator(
            base_page = 1,
            total_path = None
        )
    )

    for page in client.paginate("data_engineering_zoomcamp_api"):
        yield page

# Initialize the pipeline configuration
pipeline = dlt.pipeline(
    pipeline_name = "ny_taxi_pipeline",
    destination="duckdb",
    dataset_name = "ny_taxi_data"
)

# Run the pipeline and get loading information
load_info = pipeline.run(ny_taxi_rides)
print(load_info)

# Connect to the DuckDB database
conn = duckdb.connect(f"{pipeline.pipeline_name}.duckdb")
conn.sql(f"SET search_path = '{pipeline.dataset_name}'")

# Show what tables exist in the database
result = conn.sql("SHOW TABLES").df()
print("\nTables in database:")
print(result)

# Show the schema of the rides table
print("\nSchema for rides table:")
print(conn.sql("DESCRIBE rides").df().to_string())