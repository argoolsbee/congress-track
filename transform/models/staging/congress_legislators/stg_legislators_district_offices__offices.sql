with source as (

    select * from {{ source('congress_legislators', 'legislators_district_offices__offices') }}

),

renamed as (

    select
        _dlt_id as dlt_id,
        _dlt_parent_id as dlt_parent_id,
        _dlt_root_id as dlt_root_id,
        _dlt_list_idx as dlt_list_idx,
        id as office_id,
        address,
        suite,
        city,
        state,
        zip,
        latitude,
        longitude,
        phone,
        fax,
        building,
        hours

    from source

)

select * from renamed
