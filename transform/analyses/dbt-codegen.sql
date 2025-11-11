-- source
{#
{{ codegen.generate_source(database_name= 'congress_track', schema_name= 'congress_legislators') }}
#}

-- model sql
{#
{{ codegen.generate_base_model(
    source_name='congress_legislators',
    table_name='legislators_historical__terms__party_affiliations'
) }}
#}


-- model yml
{#
{{ codegen.generate_model_yaml(
    model_names=['customers']
) }}
#}