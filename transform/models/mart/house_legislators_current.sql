{{
    config(materialized='external', location='../load/{{ this.table }}.parquet')
}}

with legislator_term_counts as (
    select * from {{ ref('int_legislators_current') }}
)

select
    trm.official_full_name,
    trm.state_code,
    trm.state_name,
    trm.party,
    trm.term_count,
    trm.first_term_start,
    trm.last_term_end,
    trm.gender,
    trm.age,
    trm.age_first_term_start,
    trm.age_last_term_end,
    trm.years_served,
    trm.years_elected,
    trm.years_remaining
from legislator_term_counts as trm
where trm.chamber_code = 'rep'
