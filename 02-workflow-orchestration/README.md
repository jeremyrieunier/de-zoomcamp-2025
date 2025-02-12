# Module 2: Workflow Orchestration with Kestra
This module focuses on workflow orchestration using [Kestra](https://github.com/kestra-io/kestra), an open-source data orchestration and scheduling platform. The implementation includes setting up a local environment with Docker and creating data pipelines to load NYC Taxi data into PostgreSQL and BigQuery.

## Project Structure
```yaml
02-workflow-orchestration/
├── docker-compose.yaml
└── flows/
    ├── 01_getting_started.yaml                     # Basic Kestra pipeline example
    ├── 02_postgres_data_pipeline.yaml              # PostgreSQL data pipeline
    ├── 03_postgres_taxi_pipeline_scheduled.yaml    # Scheduled version for Postgres
    ├── 04_gcp_setup.yaml                           # GCP infrastructure setup
    ├── 05_gcp_taxi_pipeline.yaml                   # GCP taxi data pipeline
    └── 06_gcp_taxi_pipeline_scheduled.yaml         # Scheduled version for BigQuery
```

## Setup Instructions
### Prerequisites
- Docker and Docker Compose
- GCP account with necessary permissions (for GCP pipelines)

### Environment Setup
Start the environment:
```bash
docker-compose up -d
```

This will spin up:

- PostgreSQL database (port 5432)
- pgAdmin web interface (port 8085)
- Kestra server (port 8080)

### Accessing Services
- Kestra UI: http://localhost:8080
- pgAdmin: http://localhost:8085 (pgadmin@pgadmin.com / pgadmin)

## Pipeline Descriptions

### Getting Started Pipeline (dummy_json_getting_started.yaml)
A simple pipeline that:
- Fetches data from the [Dummy JSON API](https://dummyjson.com/)
- Processes it with Python using Polars
- Performs analysis using DuckDB
- Scheduled to run daily at 10:00 AM

### NYC Taxi Data Pipelines

#### PostgreSQL Version (postgres_taxi_pipeline.yaml)
- Downloads NYC taxi trip data
- Loads it into PostgreSQL
- Implements data quality checks and deduplication
- Available for both yellow and green taxis
- Supports manual execution with year/month selection

#### GCP Version (gcp_taxi_pipeline.yaml)
- Similar functionality to PostgreSQL version but utilises GCP services
- Stores data in Google Cloud Storage
- Loads data into BigQuery
- Implements partitioning for better query performance
- Supports both yellow and green taxi data

#### Scheduled Versions
Both PostgreSQL and GCP pipelines have scheduled variants that:
- Run automatically on the first day of each month
- Process the previous month's data
- Include proper error handling and logging
- Implement cleanup procedures

#### Environment Variables
For GCP pipelines, the following environment variables should be set up using Kestra's [Key Value (KV) Store](https://kestra.io/docs/concepts/kv-store):
- GCP_PROJECT_ID
- GCP_LOCATION
- GCP_BUCKET_NAME
- GCP_DATASET

### Key Features
- Data Deduplication: Uses MD5 hashing of key fields to create unique identifiers
- Error Handling: Implements proper error handling and logging
- Incremental Loading: Uses MERGE statements to avoid duplicates
- Data Quality: Includes data type validation and null handling
- Scheduling: Automated monthly data processing
- Infrastructure as Code: Complete setup defined in YAML