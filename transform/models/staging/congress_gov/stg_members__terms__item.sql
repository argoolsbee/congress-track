with source as (

    select * from {{ source('congress_gov', 'members__terms__item') }}

),

renamed as (

    select
        chamber,
        start_year,
        end_year,
        _dlt_root_id,
        _dlt_parent_id,
        _dlt_list_idx,
        _dlt_id

    from source

)

select * from renamed
