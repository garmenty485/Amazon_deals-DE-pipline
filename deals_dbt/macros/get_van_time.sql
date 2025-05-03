{% macro get_van_time() %}
    {% set timezone = env_var('TIMEZONE') %}
    {% do log("Current time being used: " ~ modules.datetime.datetime.now(modules.pytz.timezone(timezone)).strftime('%Y%m%d%H'), info=True) %}
    {% set van_time = modules.datetime.datetime.now(modules.pytz.timezone(timezone)).strftime('%Y%m%d%H') %}
    {{ return(van_time) }}
{% endmacro %}