use role accountadmin

TRUNCATE TABLE weather_data;

-- Create a new database 
CREATE DATABASE DE_PROJECT;

-- Switch to the newly created database
USE DATABASE DE_PROJECT;

-- Create table to load CSV data
CREATE OR REPLACE TABLE weather_data (
    city STRING,
    temp FLOAT,
    wind_dir STRING,
    humidity INTEGER,
    pressure_mb INTEGER,
    time TIMESTAMP,
    wind_speed FLOAT
);



--Create integration object for external stage
create or replace storage integration s3_int
  type = external_stage
  storage_provider = s3
  enabled = true
  storage_aws_role_arn = 'input_your_arn_role'
  storage_allowed_locations = ('s3://forsnowflake-v1/snowflake/');

  
--Describe integration object to fetch external_id and to be used in s3
DESC INTEGRATION s3_int;

create or replace file format csv_format
                    type = csv
                    field_delimiter = ','
                    skip_header = 1
                    null_if = ('NULL', 'null')
                    empty_field_as_null = true;
                    
create or replace stage ext_csv_stage
  URL = 's3://forsnowflake-v1/snowflake/'
  STORAGE_INTEGRATION = s3_int
  file_format = csv_format;

list @ext_csv_stage;

--create pipe to automate data ingestion from s3 to snowflake
create or replace pipe mypipe auto_ingest=true as
copy into weather_data
from @ext_csv_stage
on_error = CONTINUE;

show pipes;

select * from weather_data;
