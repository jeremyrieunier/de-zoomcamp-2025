with

source as (
    select *
    from {{ source("staging", "green_tripdata")}}
),

renamed as (
    select
        {{ dbt_utils.generate_surrogate_key(["VendorID", "lpep_pickup_datetime"] )}} as tripid,
        VendorID,
        lpep_pickup_datetime,
        lpep_dropoff_datetime,
        store_and_fwd_flag,
        RatecodeID,
        passenger_count,
        trip_distance,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        ehail_fee,
        improvement_surcharge,
        total_amount,
        payment_type,
        {{ get_payment_type_description("payment_type") }} as payment_type_description,
        trip_type,
        PULocationID,
        DOLocationID
    from source
)

select *
from renamed