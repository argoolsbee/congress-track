{{
    config(materialized='external', location='../load/{{ this.table }}.parquet')
}}

with legislator_offices as (
    select * from {{ ref('stg_legislators_district_offices') }}
),

legislators as (
    select * from {{ ref('int_legislators_current') }}
),

offices as (
    select * from {{ ref('stg_legislators_district_offices__offices') }}
)

select
    ofc.office_id,
    leg.dlt_id as legislator_dlt_id,
    leg.display_name,
    leg.party,
    ofc.address,
    ofc.suite,
    ofc.city,
    ofc.state,
    ofc.zip,
    ofc.latitude,
    ofc.longitude,
    ofc.phone,
    ofc.fax,
    ofc.building,
    ofc.hours
from legislator_offices as leg_ofc
left join
    legislators as leg
    on leg_ofc.bioguide_id = leg.bioguide_id
left join
    offices as ofc
    on leg_ofc.dlt_id = ofc.dlt_parent_id
