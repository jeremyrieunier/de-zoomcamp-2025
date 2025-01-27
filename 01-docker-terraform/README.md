# Docker Module
This module demonstrates how to use Docker and [Docker Compose](https://docs.docker.com/compose/) to set up a local development environment for working with the NY Taxi dataset.

## Structure
```
docker/
├── data_sources/         # Contains source data files
├── practice/             # Docker practice exercises
├── create_table.py       # Python script to create required database tables
├── docker-compose.yaml   # Defines services (Postgres + pgAdmin)
└── ingest_data.py        # Python script to load data into Postgres
```

## Key Components

### Docker Compose Setup
#### Postgres 17 (Alpine) container with:
- Database: ny_taxi
- Port: 5433
- Persistent storage via [Docker volume](https://docs.docker.com/engine/storage/volumes/)

#### pgAdmin4 container for database management
- Port: 8080
- Web interface credentials: pgadmin@pgadmin.com / pgadmin


### Python Scripts
- `create_table.py`: creates tables for taxi trips and zone lookup data using [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)
- `ingest_data.py`: processes and loads CSV data using [pandas](https://github.com/pandas-dev/pandas) into Postgres via [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)
- Handles large files through chunked processing
- Includes datetime conversion
- Error handling and progress logging

## Usage

1. Start containers:
```
docker-compose up -d
```

2. Create database tables:

```
python create_table.py
```

3. Load data:
```
python ingest_data.py
```

4. Access pgAdmin at http://localhost:8080 to interact with the database.

# Terraform Module
The module sets up GCP infrastructure using Terraform, including a [Google Cloud Storage bucket](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket.html) and [BigQuery dataset](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset).

### Infrastructure Components
GCS bucket with:
- Versioning enabled
- Uniform bucket level access
- Lifecycle rule for incomplete multipart uploads

BigQuery dataset with environment labels
- Configuration Files

- `main.tf`: Defines GCP resources
- `variables.tf`: Configures [Terraform variables](https://developer.hashicorp.com/terraform/language/values/variables) like:
- Project ID
- Region/Location
- Storage class
- Environment (dev/prod)