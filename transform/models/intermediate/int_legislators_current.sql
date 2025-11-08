with legislators_current as (

    select * from {{ ref('stg_legislators_current') }}

),

legislators_current_terms as (

    select * from {{ ref('stg_legislators_current__terms') }}

),

term_agg as (
    select
        trm.dlt_parent_id,
        trm.type_code,
        trm.type,
        trm.state,
        case trm.party when 'Independent' then 'Independent (' || trm.caucus || ')' else trm.party end as party,
        count(*) as term_count,
        min(trm.start_date) as first_term_start,
        max(trm.end_date) as last_term_end
    from legislators_current_terms as trm
    group by all
)

select
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
    trm.type_code,
    trm.type,
    trm.state,
    trm.party,
    trm.term_count,
    trm.first_term_start,
    trm.last_term_end,
    date_diff('year', leg.birthday, trm.first_term_start) as age_first_term_start,
    date_diff('year', leg.birthday, trm.last_term_end) as age_last_term_end,
    date_diff('year', trm.first_term_start, today()) as years_served,
    age_last_term_end - age_first_term_start as years_elected,
    years_elected - years_served as years_remaining,
    leg.wikidata_id
from
    legislators_current as leg
inner join
    term_agg as trm
    on leg.dlt_id = trm.dlt_parent_id
where trm.last_term_end >= today()
-- Source contains historical data for an active member's time in the other house of congress.
