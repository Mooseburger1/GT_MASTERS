
events = LOAD 'data/' USING PigStorage(',') AS (patientid:chararray, eventname:chararray, dateoffset:int, value:int);

targets = FILTER events BY eventname == 'heartfailure';

event_target_pairs = JOIN events by patientid, targets BY patientid;

filtered_events = FILTER event_target_pairs BY (events::dateoffset <= targets::dateoffset - 365);

filtered_events = FOREACH filtered_events GENERATE $0 AS patientid, $1 AS eventname, $3 AS value;

feature_name_values = GROUP filtered_events BY (patientid, eventname);

DESCRIBE feature_name_values;                                         

feature_name_values = FOREACH feature_name_values GENERATE group.$0, group.$1 as featurename, SUM(filtered_events.value) AS value;

DESCRIBE feature_name_values                                                                              

-- commented intentionally in script
-- dump feature_name_values; 

feature_names = FOREACH feature_name_values GENERATE featurename;

feature_names = DISTINCT feature_names;

feature_name_index = RANK feature_names;

feature_name_index = FOREACH feature_name_index GENERATE $0 AS index, $1;

DESCRIBE feature_name_index 

-- commented intentionally in script
-- DUMP feature_name_index; 

feature_id_values = JOIN feature_name_values BY featurename, feature_name_index BY featurename;

DESCRIBE feature_id_values;

feature_id_values = FOREACH feature_id_values GENERATE feature_name_values::patientid AS patientid, feature_name_index::index AS featureid, feature_name_values::value as value; 

DESCRIBE feature_id_values;

-- commented intentionally in script
-- DUMP feature_id_values; 

grpd = GROUP feature_id_values BY patientid;

DESCRIBE grpd;

REGISTER utils.py USING jython AS utils;

feature_vectors = FOREACH grpd {
    sorted = ORDER feature_id_values BY featureid;
    generate group as patientid, utils.bag_to_svmlight(sorted) as sparsefeature;
}

-- commented intentionally in script
-- DUMP feature_vectors; 

samples = JOIN targets BY patientid, feature_vectors BY patientid;

DESCRIBE samples;

samples = FOREACH samples GENERATE targets::value AS label, feature_vectors::sparsefeature as sparsefeature;

DESCRIBE samples;

-- commented intentionally in script
-- DUMP samples; 

samples = FOREACH samples GENERATE RANDOM() as assignmentkey, *;

SPLIT samples INTO testing IF assignmentkey <= 0.20, training OTHERWISE;

training = FOREACH training GENERATE $1..;

testing = FOREACH testing GENERATE $1..;

STORE training INTO 'training' USING PigStorage(' ');

STORE testing INTO 'testing' USING PigStorage(' ');
