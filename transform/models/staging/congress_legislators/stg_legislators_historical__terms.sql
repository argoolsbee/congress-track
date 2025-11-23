with source as (

    select * from {{ source('congress_legislators', 'legislators_historical__terms') }}

),

renamed as (

    select
        _dlt_id as dlt_id,
        _dlt_parent_id as dlt_parent_id,
        _dlt_root_id as dlt_root_id,
        _dlt_list_idx as dlt_list_idx,
        type,
        start::date as start_date,
        "end"::date as end_date,
        state,
        class,
        party,
        caucus,
        district,
        how,
        url,
        address,
        phone,
        fax,
        contact_form,
        office,
        state_rank,
        rss_url,
        end_type

    from source

)

select * from renamed
