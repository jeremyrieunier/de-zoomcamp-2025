{{
    config(
        materialized='table'
    )
}}

with green_tripdata as (
    select
        *,
        "Green" as service_type
    from {{ ref('stg_green_tripdata') }}
), 

yellow_tripdata as (
    select
        *,
        "Yellow" as service_type
    from {{ ref('stg_yellow_tripdata') }}
),

trips_unioned as (
    select *
    from green_tripdata
    union all
    select *
    from yellow_tripdata

),

dim_zone as (
    select *
    from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)

select
    trips.*,
    pickup_zone.borough as pickup_borough,
    pickup_zone.zone as pickup_zone,
    pickup_zone.service_zone as pickup_service_zone,
    dropoff_zone.borough as dropoff_borough,
    dropoff_zone.zone as dropoff_zone,
    dropoff_zone.service_zone as dropoff_service_zone
from trips_unioned as trips
inner join dim_zone as pickup_zone
    on trips.pickup_location_id = pickup_zone.location_id
inner join dim_zone as dropoff_zone
    on trips.dropoff_location_id = dropoff_zone.location_id