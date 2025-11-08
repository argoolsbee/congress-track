with

renamed as (

    select
        _dlt_id as dlt_id,
        _dlt_root_id as dlt_root_id,
        _dlt_parent_id as dlt_parent_id,
        _dlt_list_idx as dlt_list_idx,
        type as type_code,
        case type
            when 'rep' THEN 'House of Representatives'
            when 'sen' Then 'Senate'
            else type
        end as type,
        start::date as start_date,
        "end"::date as end_date,
        state,
        district,
        party,
        class,
        url,
        address,
        phone,
        fax,
        contact_form,
        office,
        state_rank,
        rss_url,
        caucus,
        how,
        end_type
    from {{ source('congress_legislators', 'legislators_current__terms') }}

)

select * from renamed
