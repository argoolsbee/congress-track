-- Requires community extension 'webbed' for html_extract_text

with source as (

    select * from {{ source('congress_gov', 'members') }}

),

renamed as (

    select
        bioguide_id,
        name,
        party_name,
        state,
        district,
        url,
        depiction__image_url as image_url,
        html_extract_text(depiction__attribution::html, '//a') as extracted_attribution_text,
        coalesce(extracted_attribution_text, depiction__attribution) as image_attribution_text,
        html_extract_text(depiction__attribution::html, '//a/@href') as image_attribution_url,
        update_date as last_update_date,
        _dlt_load_id,
        _dlt_id

    from source

)

select * from renamed
