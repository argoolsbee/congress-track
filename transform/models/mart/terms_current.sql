{{
    config(materialized='external', location='../load/{{ this.table }}.parquet')
}}

with

terms as (select * from {{ ref('stg_legislators_current__terms') }}
)

select
    dlt_id,
    dlt_root_id,
    dlt_parent_id,
    dlt_list_idx,
    chamber_code,
    chamber_name,
    start_date,
    end_date,
    state,
    district,
    party,
    class,
    url,
    address,
    phone,
    fax,
    contact_form,
    office,
    state_rank,
    rss_url,
    caucus,
    how,
    end_type
from terms
