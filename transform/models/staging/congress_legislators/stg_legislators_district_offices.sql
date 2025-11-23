with source as (

    select * from {{ source('congress_legislators', 'legislators_district_offices') }}

),

renamed as (

    select
        _dlt_id as dlt_id,
        id__bioguide as bioguide_id,
        id__govtrack as govtrack_id,
        id__thomas as thomas_id

    from source

)

select * from renamed
