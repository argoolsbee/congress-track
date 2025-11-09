with source as (

    select * from {{ ref('us_states') }}

),

renamed as (

    select
        code,
        name

    from source

)

select * from renamed
