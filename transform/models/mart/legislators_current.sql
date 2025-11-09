{{
    config(materialized='external', location='../load/{{ this.table }}.parquet')
}}

with
legislators_current as (
    select * from {{ ref('int_legislators_current') }}
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
    leg.state_code,
    leg.state_name,
    leg.chamber_code,
    leg.chamber_name,
    leg.party,
    leg.term_count,
    leg.first_term_start,
    leg.last_term_end,
    leg.gender,
    leg.birthday,
    leg.age,
    leg.age_first_term_start,
    leg.age_last_term_end,
    leg.years_served,
    leg.years_elected,
    leg.years_remaining,
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
from legislators_current as leg
