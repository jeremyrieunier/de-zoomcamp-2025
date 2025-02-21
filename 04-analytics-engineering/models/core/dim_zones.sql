{{
    config(
        materialized='table'
    )
}}

select
    locationid as location_id,
    borough,
    zone,
    -- Replace Boro Zone by Green Zone since it's only served by Green Taxis
    replace(service_zone, "Boro Zone", "Green Zone") as service_zone
from {{ ref('taxi_zone_lookup') }}