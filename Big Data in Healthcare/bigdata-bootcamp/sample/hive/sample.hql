-- If the events table exits drop it.
DROP TABLE IF EXISTS events;

-- Create the table events.  Now the text file has flat text but since we know the data types we have those here.
-- The source file is a comma delimited text file thus we need to code the table to handle that.
CREATE TABLE events (
  patient_id STRING,
  event_name STRING,
  date_offset INT,
  value INT)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
-- Load the data from the file into the table.  Should there be any data in there, which there should not, we're going to overwrite it.
LOAD DATA LOCAL INPATH 'data'
OVERWRITE INTO TABLE events;

-- Diaplay a sample of the data that is in the events table.
SELECT patient_id, count(*) 
FROM events
GROUP BY patient_id;
