with source as (

    select * from {{ source('congress_legislators', 'legislators_current__leadership_roles') }}

),

renamed as (

    select
        _dlt_id as dlt_id,
        _dlt_root_id as dlt_root_id,
        _dlt_parent_id as dlt_parent_id,
        _dlt_list_idx as dlt_list_idx,
        title,
        chamber,
        start,
        "end"

    from source

)

select * from renamed
