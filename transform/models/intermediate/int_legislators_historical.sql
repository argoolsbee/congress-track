with legislators_historical as (

    select * from {{ ref('stg_legislators_historical') }}

),

terms_historical as (

    select * from {{ ref('stg_legislators_historical__terms') }}

),

states as (

    select * from {{ ref('stg_us_states') }}

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
    from terms_historical as trm
    group by all
)

select
    leg.dlt_id,
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
    cast(trm.years_elected as int) as years_elected,
    leg.ballotpedia_id,
    leg.bioguide_id,
    leg.cspan_id,
    leg.google_entity_id,
    leg.govtrack_id,
    leg.house_history_id,
    leg.icpsr_id,
    leg.lis_id,
    leg.maplight_id,
    leg.opensecrets_id,
    leg.pictorial_id,
    leg.thomas_id,
    leg.votesmart_id,
    leg.wikidata_id,
    leg.wikipedia_id
from
    legislators_historical as leg
inner join
    term_agg as trm
    on leg.dlt_id = trm.dlt_parent_id
left join
    states as sta
    on trm.state = sta.code
