with source as (

    select * from {{ source('congress_legislators', 'legislators_historical__other_names') }}

),

renamed as (

    select
        _dlt_id as dlt_id,
        _dlt_parent_id as dlt_parent_id,
        _dlt_root_id as dlt_root_id,
        _dlt_list_idx as dlt_list_idx,
        last as last_name,
        "end"::date as end_date

    from source

)

select * from renamed
