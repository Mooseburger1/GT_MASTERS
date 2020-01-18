import utils
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# PLEASE USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT

def read_csv(filepath):
    
    '''
    TODO: This function needs to be completed.
    Read the events.csv, mortality_events.csv and event_feature_map.csv files into events, mortality and feature_map.
    
    Return events, mortality and feature_map
    '''

    #Columns in events.csv - patient_id,event_id,event_description,timestamp,value
    events = pd.read_csv(filepath + 'events.csv')
    
    #Columns in mortality_event.csv - patient_id,timestamp,label
    mortality = pd.read_csv(filepath + 'mortality_events.csv')

    #Columns in event_feature_map.csv - idx,event_id
    feature_map = pd.read_csv(filepath + 'event_feature_map.csv')

    return events, mortality, feature_map


def calculate_index_date(events, mortality, deliverables_path):
    
    '''
    TODO: This function needs to be completed.

    Refer to instructions in Q3 a

    Suggested steps:
    1. Create list of patients alive ( mortality_events.csv only contains information about patients deceased)
    2. Split events into two groups based on whether the patient is alive or deceased
    3. Calculate index date for each patient
    
    IMPORTANT:
    Save indx_date to a csv file in the deliverables folder named as etl_index_dates.csv. 
    Use the global variable deliverables_path while specifying the filepath. 
    Each row is of the form patient_id, indx_date.
    The csv file should have a header 
    For example if you are using Pandas, you could write: 
        indx_date.to_csv(deliverables_path + 'etl_index_dates.csv', columns=['patient_id', 'indx_date'], index=False)

    Return indx_date
    '''
    #join data to filter alive vs dead patients
    data = pd.merge(left=events, right=mortality, how = 'outer', 
                    on='patient_id', suffixes=('_events', '_dead'))
    data['label'] = data.label.fillna(0.0)
    dead_data = data[data.label == 1.0]
    alive_data = data[data.label == 0.0]

    #find alive patient index dates
    alive_index_dates = alive_data.groupby('patient_id')['timestamp_events'].\
                        apply(list).apply(np.unique).apply(sorted).\
                        apply(lambda x: x[-1]).reset_index().\
                        rename(columns={'timestamp_events':'indx_date'})

    #find dead patient index dates
    dead_data['timestamp_dead'] = pd.to_datetime(dead_data.timestamp_dead.values)
    dead_index_dates = dead_data.groupby('patient_id')['timestamp_dead'].\
                       apply(np.unique).apply(lambda x: x[0] - np.timedelta64(30,'D')).\
                       apply(lambda x: x.strftime('%Y-%m-%d')).\
                       reset_index().rename(columns={'timestamp_dead':'indx_date'})
    


    indx_date = pd.concat([alive_index_dates, dead_index_dates]).reset_index().drop('index', axis = 1)
    indx_date.to_csv(deliverables_path + 'etl_index_dates.csv', columns=['patient_id', 'indx_date'], index=False)
    
    return indx_date


def filter_events(events, indx_date, deliverables_path):
    
    '''
    TODO: This function needs to be completed.

    Refer to instructions in Q3 b

    Suggested steps:
    1. Join indx_date with events on patient_id
    2. Filter events occuring in the observation window(IndexDate-2000 to IndexDate)
    
    
    IMPORTANT:
    Save filtered_events to a csv file in the deliverables folder named as etl_filtered_events.csv. 
    Use the global variable deliverables_path while specifying the filepath. 
    Each row is of the form patient_id, event_id, value.
    The csv file should have a header 
    For example if you are using Pandas, you could write: 
        filtered_events.to_csv(deliverables_path + 'etl_filtered_events.csv', columns=['patient_id', 'event_id', 'value'], index=False)

    Return filtered_events
    '''

    #merge data
    data=pd.merge(left=events, right=indx_date, how='outer', on='patient_id')
    
    #convert data type to datetime
    data.timestamp = pd.to_datetime(data.timestamp.values)
    data.indx_date = pd.to_datetime(data.indx_date.values)
    
    #calculate time delta between index and event timestamps
    data['time_delta'] = (data.indx_date - data.timestamp).dt.days.astype('int')

    #filter for time deltas greater than 0 & less than or equal to 2000
    filtered_events = data[(data.time_delta >= 0) & (data.time_delta <=2000)].loc[:,['patient_id','event_id','value']]
    
    

    #write to deliverables
    filtered_events.to_csv(deliverables_path + 'etl_filtered_events.csv', columns=['patient_id', 'event_id', 'value'], index=False)
    
    return filtered_events


def aggregate_events(filtered_events_df, mortality_df,feature_map_df, deliverables_path):
    
    '''
    TODO: This function needs to be completed.

    Refer to instructions in Q3 c

    Suggested steps:
    1. Replace event_id's with index available in event_feature_map.csv
    2. Remove events with n/a values
    3. Aggregate events using sum and count to calculate feature value
    4. Normalize the values obtained above using min-max normalization(the min value will be 0 in all scenarios)
    
    
    IMPORTANT:
    Save aggregated_events to a csv file in the deliverables folder named as etl_aggregated_events.csv. 
    Use the global variable deliverables_path while specifying the filepath. 
    Each row is of the form patient_id, event_id, value.
    The csv file should have a header .
    For example if you are using Pandas, you could write: 
        aggregated_events.to_csv(deliverables_path + 'etl_aggregated_events.csv', columns=['patient_id', 'feature_id', 'feature_value'], index=False)

    Return filtered_events
    '''
    #create a feature mapper dictionary
    mapper = feature_map_df.set_index('event_id').to_dict()['idx']
    
    #map event_id to index values
    filtered_events_df['feature_id'] = filtered_events_df.event_id.apply(lambda x: mapper[x])
    
    #drop null values
    filtered_events_df = filtered_events_df.dropna(subset=['value'])
    
    #agg events
    filtered_events_df['dummy_value'] = filtered_events_df.value
    filtered_events_df = filtered_events_df.groupby(['patient_id','feature_id', 'event_id']).\
                      agg({'value':'sum', 'dummy_value':'count'}).\
                      rename(columns={'value':'sum', 'dummy_value':'count'}).\
                      reset_index()
    
    def selection(event, sum_, count):
        if 'LAB' in event:
            return count
        else:
            return sum_
        
    filtered_events_df['feature_value'] = filtered_events_df[['event_id', 'sum', 'count']].apply(lambda x: selection(*x), axis = 1)
    aggregated_events = filtered_events_df.loc[:,['patient_id', 'feature_id', 'feature_value']]
    
    #Normalize data
    def norm(id_, value, max_dict):
        max_ = max_dict[id_]
        return value/max_

    max_dict = aggregated_events.groupby('feature_id')['feature_value'].apply(max)
    aggregated_events.feature_value = aggregated_events[['feature_id','feature_value']].apply(lambda x: norm(*x, max_dict),axis=1)
    
    
    #write to csv
    if deliverables_path == '_':
        return aggregated_events
        
    aggregated_events.to_csv(deliverables_path + 'etl_aggregated_events.csv', columns=['patient_id', 'feature_id', 'feature_value'], index=False)
    
    return aggregated_events

def create_features(events, mortality, feature_map):
    
    deliverables_path = '../deliverables/'

    #Calculate index date
    indx_date = calculate_index_date(events, mortality, deliverables_path)

    #Filter events in the observation window
    filtered_events = filter_events(events, indx_date,  deliverables_path)
    
    #Aggregate the event values for each patient 
    aggregated_events = aggregate_events(filtered_events, mortality, feature_map, deliverables_path)

    '''
    TODO: Complete the code below by creating two dictionaries - 
    1. patient_features :  Key - patient_id and value is array of tuples(feature_id, feature_value)
    2. mortality : Key - patient_id and value is mortality label
    '''
    grp = aggregated_events.groupby('patient_id').agg(list)
    
    def tuples(x,y):
        return zip(x,y)

    patient_features = pd.Series.to_dict(grp[['feature_id','feature_value']].apply(lambda x: list(tuples(*x)), axis = 1))
    
    data = pd.merge(left=events, right=mortality, how = 'outer', 
                    on='patient_id', suffixes=('_events', '_dead'))
    data['label'] = data.label.fillna(0.0)
    mortality = pd.Series.to_dict(data.groupby('patient_id')['label'].apply(list).apply(np.unique).apply(lambda x: x[0]))


    return patient_features, mortality

def save_svmlight(patient_features, mortality, op_file, op_deliverable):
    
    '''
    TODO: This function needs to be completed

    Refer to instructions in Q3 d

    Create two files:
    1. op_file - which saves the features in svmlight format. (See instructions in Q3d for detailed explanation)
    2. op_deliverable - which saves the features in following format:
       patient_id1 label feature_id:feature_value feature_id:feature_value feature_id:feature_value ...
       patient_id2 label feature_id:feature_value feature_id:feature_value feature_id:feature_value ...  
    
    Note: Please make sure the features are ordered in ascending order, and patients are stored in ascending order as well.     
    '''
    deliverable1 = open(op_file, 'wb')
    deliverable2 = open(op_deliverable, 'wb')
    
    #svmlight
    for k in patient_features.keys():
        patient_features[k] = sorted(patient_features[k])
        deliverable1.write(bytes(("{} ".format(int(mortality[k]))),'UTF-8'))
        for v in patient_features[k]:
            deliverable1.write(bytes(("{}:{:.6f} ".format(v[0],v[1])),'UTF-8'))
        deliverable1.write(bytes(("\n"),'UTF-8'))

    deliverable1.close()
    
    #svm
    for k in patient_features.keys():
        deliverable2.write(bytes(("{} {} ".format(int(k), int(mortality[k]))),'UTF-8'))
        for v in patient_features[k]:
            deliverable2.write(bytes(("{}:{:.6f} ".format(int(v[0]),round(v[1],6))),'UTF-8'))
        deliverable2.write(bytes(("\n"),'UTF-8'))


    deliverable2.close()

def main():
    train_path = '../data/train/'
    events, mortality, feature_map = read_csv(train_path)
    patient_features, mortality = create_features(events, mortality, feature_map)
    save_svmlight(patient_features, mortality, '../deliverables/features_svmlight.train', '../deliverables/features.train')

if __name__ == "__main__":
    main()