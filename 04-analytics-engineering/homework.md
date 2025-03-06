# Module 4 Homework: Analytics Engineering with dbt

## Question 1: Understanding dbt model resolution
Provided you've got the following sources.yaml

```yaml
version: 2

sources:
  - name: raw_nyc_tripdata
    database: "{{ env_var('DBT_BIGQUERY_PROJECT', 'dtc_zoomcamp_2025') }}"
    schema:   "{{ env_var('DBT_BIGQUERY_SOURCE_DATASET', 'raw_nyc_tripdata') }}"
    tables:
      - name: ext_green_taxi
      - name: ext_yellow_taxi

```

with the following env variables setup where dbt runs:

```shell
export DBT_BIGQUERY_PROJECT=myproject
export DBT_BIGQUERY_DATASET=my_nyc_tripdata
```

What does this .sql model compile to?
```sql
select * 
from {{ source('raw_nyc_tripdata', 'ext_green_taxi' ) }}
```

- `select * from dtc_zoomcamp_2025.raw_nyc_tripdata.ext_green_taxi`
- `select * from dtc_zoomcamp_2025.my_nyc_tripdata.ext_green_taxi`
- **`select * from myproject.raw_nyc_tripdata.ext_green_taxi`**
- `select * from myproject.my_nyc_tripdata.ext_green_taxi`
- `select * from dtc_zoomcamp_2025.raw_nyc_tripdata.green_taxi`

### Explanation
The compilation process works as follows:
1. dbt looks up the source named `raw_nyc_tripdata` in `sources.yaml`
2. Then use the `env_var()` function to:
     - Look for the environment variable `DBT_BIGQUERY_PROJECT` and if not found, use `dtc_zoomcamp_2025` as default
     - Look for the environment variable `DBT_BIGQUERY_SOURCE_DATASET` and if not found, use `raw_nyc_tripdata` as default
3. It resolves the database value using the environment variable setup
    - For database, it uses `myproject` (from `DBT_BIGQUERY_PROJECT`)
    - For schema, since there's no `DBT_BIGQUERY_SOURCE_DATASET` variable, it uses the default value `raw_nyc_tripdata`
4. It finds the table `ext_green_taxi` defined in the source

Therefore, the SQL compiles to:
`select * from myproject.raw_nyc_tripdata.ext_green_taxi`

## Question 2: dbt Variables & Dynamic Models

Say you have to modify the following dbt_model (`fct_recent_taxi_trips.sql`) to enable Analytics Engineers to dynamically control the date range. 

- In development, you want to process only **the last 7 days of trips**
- In production, you need to process **the last 30 days** for analytics

```sql
select *
from {{ ref('fact_taxi_trips') }}
where pickup_datetime >= CURRENT_DATE - INTERVAL '30' DAY
```

What would you change to accomplish that in a such way that command line arguments takes precedence over ENV_VARs, which takes precedence over DEFAULT value?

- Add `ORDER BY pickup_datetime DESC` and `LIMIT {{ var("days_back", 30) }}`
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", 30) }}' DAY`
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ env_var("DAYS_BACK", "30") }}' DAY`
- **Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30")) }}' DAY`**
- Update the WHERE clause to `pickup_datetime >= CURRENT_DATE - INTERVAL '{{ env_var("DAYS_BACK", var("days_back", "30")) }}' DAY`

### Explanation
The solution uses a nested approach to create the right precedence chain:

Command line args → Environment variables → Default value
1. The `var("days_back", env_var("DAYS_BACK", "30"))` function first checks if a variable was passed via command line (e.g `--vars '{"days_back": 7}'`)
2. If no command line argument is provided, it falls back to environment variables and checks for an environment variable called `DAYS_BACK`.
3. If neither command line nor environment variable is set, it uses the default value of `30`


## Question 3: dbt Data Lineage and Execution

Considering the data lineage below **and** that taxi_zone_lookup is the **only** materialization build (from a .csv seed file):

![image](https://raw.githubusercontent.com/DataTalksClub/data-engineering-zoomcamp/refs/heads/main/cohorts/2025/04-analytics-engineering/homework_q2.png)

Select the option that does **NOT** apply for materializing `fct_taxi_monthly_zone_revenue`:

- `dbt run`
- `dbt run --select +models/core/dim_taxi_trips.sql+ --target prod`
- `dbt run --select +models/core/fct_taxi_monthly_zone_revenue.sql`
- `dbt run --select +models/core/`
- **`dbt run --select models/staging/+`**

### Explanation

The `dbt run --select models/staging/+` command would fail to properly materialise the target model because dbt selects all models in the staging directory and their downstream dependencies.

However, the staging models (like `stg_green_tripdata` and `stg_yellow_tripdata`) depend on source tables (the `raw_nyc_tlc_record_data.ext_green_taxi` and `raw_nyc_tlc_record_data.ext_yellow_taxi` tables). These source tables are upstream dependencies that wouldn't be included in this selection pattern. 

Without ensuring these source tables are properly configured and available, the staging models can't be built successfully. Since the staging models are prerequisites for building `fct_taxi_monthly_zone_revenue`, this command wouldn't work for materialising the target model.