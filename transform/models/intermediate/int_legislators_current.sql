with legislators_current as (

    select * from {{ ref('stg_legislators_current') }}

),

terms_current as (

    select * from {{ ref('stg_legislators_current__terms') }}

),

social_media as (

    select * from {{ ref('stg_legislators_social_media') }}

),

states as (

    select * from {{ ref('stg_us_states') }}

),

members as (

    select * from {{ ref('stg_members') }}

),

term_agg as (
    select
        trm.dlt_parent_id,
        trm.chamber_code,
        trm.chamber_name,
        trm.state,
        case trm.party when 'Independent' then 'Independent (' || trm.caucus || ')' else trm.party end as party,
        count(*) as term_count,
        min(trm.start_date) as first_term_start,
        max(trm.end_date) as last_term_end,
        sum(date_diff('year', trm.start_date, trm.end_date)) as years_elected
    from terms_current as trm
    group by all
)

select
    leg.dlt_id,
    leg.bioguide_id,
    leg.official_full_name,
    leg.display_name,
    leg.first_name,
    leg.middle_name,
    leg.last_name,
    leg.name_suffix,
    leg.nickname,
    leg.birthday,
    leg.gender,
    date_diff('year', leg.birthday, today()) as age,
    trm.chamber_code,
    trm.chamber_name,
    trm.state as state_code,
    sta.name as state_name,
    trm.party,
    trm.term_count,
    trm.first_term_start,
    trm.last_term_end,
    date_diff('year', leg.birthday, trm.first_term_start) as age_first_term_start,
    date_diff('year', leg.birthday, trm.last_term_end) as age_last_term_end,
    age_last_term_end - age as years_remaining,
    cast(trm.years_elected as int) as years_elected,
    cast(years_elected - years_remaining as int) as years_served,
    'https://ballotpedia.org/' || leg.ballotpedia_id as ballotpedia_url,
    'https://bioguide.congress.gov/search/bio/' || leg.bioguide_id as bioguide_url,
    -- leg.cspan_id,
    'https://www.google.com/search?kgmid='
    || substring(leg.google_entity_id from position(':' in leg.google_entity_id) + 1) as google_knowledge_graph_url,
    'https://www.govtrack.us/congress/members/' || leg.govtrack_id as govtrack_url,
    -- leg.house_history_id,
    -- leg.icpsr_id,
    -- leg.lis_id,
    -- leg.maplight_id,
    -- leg.opensecrets_id,
    -- leg.pictorial_id,
    -- leg.thomas_id,
    -- leg.votesmart_id,
    'https://www.wikidata.org/wiki/' || leg.wikidata_id as wikidata_url,
    'https://www.wikipedia.org/wiki/' || leg.wikipedia_id as wikipedia_url,
    som.facebook_handle,
    som.facebook_url,
    som.instagram_handle,
    som.instagram_url,
    som.mastodon_handle,
    som.mastodon_url,
    som.twitter_handle,
    som.twitter_url,
    som.youtube_handle,
    som.youtube_url,
    mem.image_url,
    mem.image_attribution_text,
    mem.image_attribution_url
from
    legislators_current as leg
inner join
    term_agg as trm
    on leg.dlt_id = trm.dlt_parent_id
left join
    social_media as som
    on leg.bioguide_id = som.bioguide_id
left join
    states as sta
    on trm.state = sta.code
left join
    members as mem
    on leg.bioguide_id = mem.bioguide_id
where trm.last_term_end >= today()
-- Source contains historical data for an active member's time in the other house of congress.
