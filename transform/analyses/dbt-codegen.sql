-- source

-- {{ codegen.generate_source(database_name= 'congress_legislators', schema_name= 'legislators_current') }}


-- model sql

-- {{ codegen.generate_base_model(
--     source_name='congress_legislators',
--     table_name='legislators_current'
-- ) }}


-- model yml

-- {{ codegen.generate_model_yaml(
--     model_names=['customers']
-- ) }}
