{{
    config(materialized='external', location='../load/{{ this.table }}.parquet')
}}

with
legislator_term_counts as (
    select * from {{ ref('int_legislators_current') }}
)

select
    trm.official_full_name,
    trm.display_name,
    trm.first_name,
    trm.middle_name,
    trm.last_name,
    trm.name_suffix,
    trm.nickname,
    trm.state,
    trm.type,
    trm.party,
    trm.term_count,
    trm.first_term_start,
    trm.last_term_end,
    trm.gender,
    trm.birthday,
    trm.age,
    trm.age_first_term_start,
    trm.age_last_term_end,
    trm.years_served,
    trm.years_elected,
    trm.years_remaining
from legislator_term_counts as trm
