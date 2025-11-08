with

renamed as (

    select
        _dlt_id as dlt_id,
        id__bioguide as bioguide_id,
        id__thomas as thomas_id,
        id__lis as lis_id,
        id__govtrack as govtrack_id,
        id__opensecrets as opensecrets_id,
        id__votesmart as votesmart_id,
        id__cspan as cspan_id,
        id__wikipedia as wikipedia_id,
        id__house_history as house_history_id,
        id__ballotpedia as ballotpedia_id,
        id__maplight as maplight_id,
        id__icpsr as icpsr_id,
        id__wikidata as wikidata_id,
        id__google_entity_id as google_entity_id,
        id__pictorial as pictorial_id,
        name__first as first_name,
        name__middle as middle_name,
        name__last as last_name,
        coalesce(name__official_full, name__first || ' ' || name__last) as official_full_name,
        name__nickname as nickname,
        name__suffix as name_suffix,
        concat_ws(' ', first_name, middle_name, last_name, name_suffix) as display_name,
        bio__birthday::date as birthday,
        bio__gender as gender
    from {{ source('congress_legislators', 'legislators_current') }}

)

select * from renamed
