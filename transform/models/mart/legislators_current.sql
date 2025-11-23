{{
    config(materialized='external', location='../load/{{ this.table }}.parquet')
}}

with
legislators_current as (
    select * from {{ ref('int_legislators_current') }}
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
    leg.ballotpedia_url,
    leg.bioguide_url,
    leg.google_knowledge_graph_url,
    leg.govtrack_url,
    leg.wikidata_url,
    leg.wikipedia_url,
    leg.facebook_handle,
    leg.facebook_url,
    leg.instagram_handle,
    leg.instagram_url,
    leg.mastodon_handle,
    leg.mastodon_url,
    leg.twitter_handle,
    leg.twitter_url,
    leg.youtube_handle,
    leg.youtube_url,
    leg.image_url,
    leg.image_attribution_text,
    leg.image_attribution_url
from legislators_current as leg
