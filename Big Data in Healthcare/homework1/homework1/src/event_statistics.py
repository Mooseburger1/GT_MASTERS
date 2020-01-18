import time
import pandas as pd
import numpy as np

# PLEASE USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT

def read_csv(filepath):
    '''
    TODO : This function needs to be completed.
    Read the events.csv and mortality_events.csv files. 
    Variables returned from this function are passed as input to the metric functions.
    '''
    events = pd.read_csv(filepath + 'events.csv')
    mortality = pd.read_csv(filepath + 'mortality_events.csv')

    return events, mortality

def event_count_metrics(events, mortality):
    '''
    TODO : Implement this function to return the event count metrics.
    Event count is defined as the number of events recorded for a given patient.
    '''
    
    data = pd.merge(left=events, right=mortality, how='outer', on='patient_id', suffixes=('_event', '_dead')).rename(columns={'label':'dead'})
    data['dead'] = data.dead.fillna(0.0)
    
    dead_data = data[data.dead == 1.0]
    alive_data = data[data.dead == 0.0]
    
    dead_stats = dead_data.groupby('patient_id')['event_id'].count().describe()
    alive_stats = alive_data.groupby('patient_id')['event_id'].count().describe()
    
    avg_dead_event_count = dead_stats['mean']
    max_dead_event_count = dead_stats['max']
    min_dead_event_count = dead_stats['min']
    avg_alive_event_count = alive_stats['mean']
    max_alive_event_count = alive_stats['max']
    min_alive_event_count = alive_stats['min']
    
    
    
    return min_dead_event_count, max_dead_event_count, avg_dead_event_count, min_alive_event_count, max_alive_event_count, avg_alive_event_count

def encounter_count_metrics(events, mortality):
    '''
    TODO : Implement this function to return the encounter count metrics.
    Encounter count is defined as the count of unique dates on which a given patient visited the ICU. 
    '''
    
    data = pd.merge(left=events, right=mortality, how='outer', on='patient_id', suffixes=('_event', '_dead')).rename(columns={'label':'dead'})
    data['dead'] = data.dead.fillna(0.0)
    
    dead_data = data[data.dead == 1.0]
    alive_data = data[data.dead == 0.0]
    
    dead_encounter_stats = dead_data.groupby('patient_id')['timestamp_event'].unique().apply(lambda x: len(x)).describe()
    alive_encounter_stats = alive_data.groupby('patient_id')['timestamp_event'].unique().apply(lambda x: len(x)).describe()
    
    avg_dead_encounter_count = dead_encounter_stats['mean']
    max_dead_encounter_count = dead_encounter_stats['max']
    min_dead_encounter_count = dead_encounter_stats['min'] 
    avg_alive_encounter_count = alive_encounter_stats['mean']
    max_alive_encounter_count = alive_encounter_stats['max']
    min_alive_encounter_count = alive_encounter_stats['min']

    return min_dead_encounter_count, max_dead_encounter_count, avg_dead_encounter_count, min_alive_encounter_count, max_alive_encounter_count, avg_alive_encounter_count

def record_length_metrics(events, mortality):
    '''
    TODO: Implement this function to return the record length metrics.
    Record length is the duration between the first event and the last event for a given patient. 
    '''
    
    data = pd.merge(left=events, right=mortality, how='outer', on='patient_id', suffixes=('_event', '_dead')).rename(columns={'label':'dead'})
    data['dead'] = data.dead.fillna(0.0)
    data['timestamp_event'] = pd.to_datetime(data.timestamp_event.values)
    
    dead_data = data[data.dead == 1.0]
    alive_data = data[data.dead == 0.0]
    
    dead_days_stats = dead_data.groupby('patient_id')['timestamp_event'].apply(np.unique).apply(sorted).apply(lambda x: x[-1] - x[0]).apply(lambda x: x.days).describe()
    alive_days_stats = alive_data.groupby('patient_id')['timestamp_event'].apply(np.unique).apply(sorted).apply(lambda x: x[-1] - x[0]).apply(lambda x: x.days).describe()
    
    avg_dead_rec_len = dead_days_stats['mean']
    max_dead_rec_len = dead_days_stats['max']
    min_dead_rec_len = dead_days_stats['min']
    avg_alive_rec_len = alive_days_stats['mean']
    max_alive_rec_len = alive_days_stats['max']
    min_alive_rec_len = alive_days_stats['min']

    return min_dead_rec_len, max_dead_rec_len, avg_dead_rec_len, min_alive_rec_len, max_alive_rec_len, avg_alive_rec_len


def main():
    '''
    DO NOT MODIFY THIS FUNCTION.
    '''
    # You may change the following path variable in coding but switch it back when submission.
    train_path = '../data/train/'

    # DO NOT CHANGE ANYTHING BELOW THIS ----------------------------
    events, mortality = read_csv(train_path)

    #Compute the event count metrics
    start_time = time.time()
    event_count = event_count_metrics(events, mortality)
    end_time = time.time()
    print(("Time to compute event count metrics: " + str(end_time - start_time) + "s"))
    print(event_count)

    #Compute the encounter count metrics
    start_time = time.time()
    encounter_count = encounter_count_metrics(events, mortality)
    end_time = time.time()
    print(("Time to compute encounter count metrics: " + str(end_time - start_time) + "s"))
    print(encounter_count)

    #Compute record length metrics
    start_time = time.time()
    record_length = record_length_metrics(events, mortality)
    end_time = time.time()
    print(("Time to compute record length metrics: " + str(end_time - start_time) + "s"))
    print(record_length)
    
if __name__ == "__main__":
    main()
