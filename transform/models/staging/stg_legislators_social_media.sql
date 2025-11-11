with source as (

    select * from {{ source('congress_legislators', 'legislators_social_media') }}

),

renamed as (

    select
        _dlt_id as dlt_id,
        id__bioguide as bioguide_id,
        id__govtrack as govtrack_id,
        id__thomas as thomas_id,
        social__facebook as facebook_handle,
        'https://www.facebook.com/' || social__facebook as facebook_url,
        social__instagram_id as instagram_id,
        social__instagram as instagram_handle,
        'https://www.instagram.com/' || social__instagram as instagram_url,
        social__mastodon as mastodon_handle,
        'https://'
        || split_part(social__mastodon, '@', 3)
        || '/@'
        || split_part(social__mastodon, '@', 2) as mastodon_url,
        social__twitter_id as twitter_id,
        social__twitter as twitter_handle,
        'https://twitter.com/' || social__twitter as twitter_url,
        social__youtube_id as youtube_id,
        social__youtube as youtube_handle,
        'https://www.youtube.com/' || social__youtube as youtube_url

    from source

)

select * from renamed
