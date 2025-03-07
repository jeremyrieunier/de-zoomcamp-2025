{{
    config(
        materialized='table'
    )
}}

with trips_data as (
    select *
    from {{ ref('fact_trips') }}
)

select
    pickup_zone as zone,
    {{ dbt.date_trunc("month", "pickup_datetime")}} as month,
    service_type,
    sum(fare_amount) as monthly_revenue_fare,
    sum(extra) as monthly_revenue_extra,
    sum(mta_tax) as monthly_revenue_mta,
    sum(tip_amount) as monthly_revenue_tip_amount,
    sum(tolls_amount) as monthly_revenue_tolls_amount,
    sum(ehail_fee) as monthly_revenue_ehail_fee,
    sum(improvement_surcharge) as monthly_revenue_improvement_surcharge,
    sum(total_amount) as monthly_revenue__total_amount,
    count(trip_id) as total_monthly_trips,
    round(avg(passenger_count), 2) as avg_monthly_passenger_count,
    round(avg(trip_distance), 2) as avg_monthly_trip_distance
from trips_data
group by zone, month, service_type