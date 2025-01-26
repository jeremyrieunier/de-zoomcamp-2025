# Module 1 Homework: Docker

## Question 1: Understanding docker first run
Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint bash.

What's the version of `pip` in the image?

- <mark>24.3.1</mark>
- 24.2.1
- 23.3.1
- 23.2.1

I ran the following command on ubuntu:
`docker run -it --entrypoint=bash python:3.12.8`

Command breakdown:
- `docker run` creates and starts a new container
- `it` enable interative mode with my terminal
- `--entrypoint=bash` overrides the default entrypoint with bash
- `python:3.12.8` specifies the Python image and version to use

After running this command and getting the shell prompt, running `pip --version` shows the pip version installed in the container, which is `24.3.1`.


## Question 2. Understanding Docker networking and docker-compose
Given the following `docker-compose.yaml`, what is the hostname and port that pgadmin should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- postgres:5433
- localhost:5432
- db:5433
- postgres:5432
- <mark>db:5432</mark>

The docker-compose.yaml file defines two services:

PostgreSQL Database Service (`db`):
- Uses [Postres 17 Alpine](https://github.com/docker-library/postgres/blob/172544062d1031004b241e917f5f3f9dfebc0df5/17/alpine3.20/Dockerfile) Alpine image
- Internal container port: `5432`
- Host machine port mapping: `5433`
- Contains database configuration (users, passwords, etc.)

pgAdmin Service (pgadmin):
- Internal container port: `80`
- Host machine port mapping: `8080`
- Contains admin interface configuration

When connecting from pgAdmin to Postgres within Docker's network

The answer is then the service name `db` with the post `5432`.

## Question 3. Trip Segmentation Count
During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:

- Up to 1 mile
- In between 1 (exclusive) and 3 miles (inclusive),
- In between 3 (exclusive) and 7 miles (inclusive),
- In between 7 (exclusive) and 10 miles (inclusive),
- Over 10 miles

Answers:

- 104,802; 197,670; 110,612; 27,831; 35,281
- <mark>104,802; 198,924; 109,603; 27,678; 35,189</mark>
- 104,793; 201,407; 110,612; 27,831; 35,281
- 104,793; 202,661; 109,603; 27,678; 35,189
- 104,838; 199,013; 109,645; 27,688; 35,202

Query used to answer the question:

```sql
select
	case
    when trip_distance <= 1 then '1 mile'
    when trip_distance > 1 and trip_distance <= 3 then '1-3 miles' 
    when trip_distance > 3 and trip_distance <= 7 then '3-7 miles'
    when trip_distance > 7 and trip_distance <= 10 then '7-10 miles'
    else 'Over 10 miles'
  end as distance_category,
	count(*) as number_of_trips
from green_taxi_trips_2019_10
where date(lpep_pickup_datetime) >= '2019-10-01' 
	and date(lpep_dropoff_datetime) < '2019-11-01'
group by distance_category
order by distance_category;
```

Output:

| distance_category | number_of_trips |
| ----------------- | --------------- |
| 1 mile | 104802 |
| 1-3 miles | 198924 |
| 3-7 miles |	109603 |
| 7-10 miles | 27678 |
| Over 10 miles | 35189 |

## Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

Tip: For every day, we only care about one single trip with the longest distance.

- 2019-10-11
- 2019-10-24
- 2019-10-26
- <mark>2019-10-31</mark>

Query used to anwer the question:

```sql
select
	date(lpep_pickup_datetime) as date,
	max(trip_distance) as longest_trip
from green_taxi_trips_2019_10
group by date
order by longest_trip desc
limit 1;
```

Output:

| date | longest_trip |
| ---- | ------------ |
| 2019-10-31 23:23:41 | 515.89 |


## Question 5. Three biggest pickup zones
Which were the top pickup locations with over 13,000 in `total_amount` (across all trips) for 2019-10-18?

Consider only `lpep_pickup_datetime` when filtering by date.

- <mark>East Harlem North, East Harlem South, Morningside Heights</mark>
- East Harlem North, Morningside Heights
- Morningside Heights, Astoria Park, East Harlem South
- Bedford, East Harlem North, Astoria Park

Query used to anwer the question:

```sql
select
	lookup.zone as pickup_location,
	sum(trips.total_amount) as total_amount
from green_taxi_trips_2019_10 trips
left join taxi_zone_lookup lookup
	on trips.pulocationid = lookup.locationid
where date(trips.lpep_pickup_datetime) = '2019-10-18'
group by lookup.zone
having sum(trips.total_amount) > 13000
order by total_amount desc
```

Output:
| zone | total_amount |
| ---- | ------------ |
| East Harlem North | 18686.68 |
| East Harlem South | 16797.26 |
| Morningside Heights | 13029.79 |


## Question 6. Largest tip
For the passengers picked up in October 2019 in the zone named "East Harlem North" which was the drop off zone that had the largest tip?

Note: it's `ti`p , not `trip`

We need the name of the zone, not the ID.

- Yorkville West
- <mar>JFK Airport</mark>
- East Harlem North
- East Harlem South

Query used to anwer the question:

```sql
select
	pickup.zone as pickup_location,
	dropoff.zone as dropoff_location,
	trips.tip_amount
from green_taxi_trips_2019_10 trips
left join taxi_zone_lookup pickup
	on trips.pulocationid = pickup.locationid
left join taxi_zone_lookup dropoff
	on trips.dolocationid = dropoff.locationid
where date(trips.lpep_pickup_datetime) between '2019-10-01' and '2019-10-31'
	and pickup.zone = 'East Harlem North'
order by trips.tip_amount desc
limit 1;
```

Output:
| pickup_location | dropoff_location | tip_amount |
| ----------- | ------------ | ---------- |
| East Harlem North | JFK Airport | 87.30 |

## Question 7. Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:

1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

Answers:

- terraform import, terraform apply -y, terraform destroy
- teraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- terraform init, terraform apply -auto-approve, terraform destroy
- terraform import, terraform apply -y, terraform rm
