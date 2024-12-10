import pandas as pd

def import_activity_data():
    # import my training data
    df = pd.read_csv('data/activities.csv')

    # drop any columns that are not needed for training the model
    df = (df
        .drop('Description', axis='columns')
        .drop('Activity Parent', axis='columns')
        .drop('Privacy', axis='columns')
        .drop('Gear', axis='columns')
        .drop('Time Zone', axis='columns')
        .drop('Offset', axis='columns')
        .drop('Activity ID', axis='columns')
        .drop('Activity Name', axis='columns')
        .drop('Location Name', axis='columns')
        .drop('File Format', axis='columns')
        .drop('Average Moving Speed (km/h or min/km)', axis='columns')
        .drop('Max. Speed (km/h or min/km)', axis='columns')
        .drop('Elapsed Duration (h:m:s)', axis='columns')
        .drop('Moving Duration (h:m:s)', axis='columns')
        .drop('Average Speed (km/h or min/km)', axis='columns')
        .drop('Device', axis='columns')
        .drop('Begin Latitude (°DD)', axis='columns')
        .drop('End Latitude (°DD)', axis='columns')
        .drop('Begin Longitude (°DD)', axis='columns')
        .drop('End Longitude (°DD)', axis='columns')
        .drop('Strokes', axis='columns')
        .drop('Elevation Corrected', axis='columns')
    )
    
    # convert columns to convenient data type for further processing
    df['Start Time'] = pd.to_datetime(df['Start Time'], utc=True)
    df['End Time'] = pd.to_datetime(df['End Time'], utc=True)
    df['Duration (h:m:s)'] = pd.to_timedelta(df['Duration (h:m:s)'])

    return df

def drop_erroneous_rows(df):
    # max speed recorded by usain bolt: https://en.wikipedia.org/wiki/Footspeed
    max_allowed_running_speed_in_kmh = 44.72
    # land speed record on a bicycle: https://en.wikipedia.org/wiki/List_of_cycling_records
    max_allowed_cycling_speed_in_kmh = 296.009

    # filter out all running activities that exceed the maximum allowed speed
    df = df[
        ~(((df['Activity Type'] == 'Running') |
           (df['Activity Type'] == 'Trail Running') |
           (df['Activity Type'] == 'Treadmill Running')) &
           (df['Max. Speed (km/h)'] >= max_allowed_running_speed_in_kmh)
        )
    ]

    # filter out all cycling activities that exceed the maximum allowed speed
    df = df[
        ~(((df['Activity Type'] == 'Cycling') |
           (df['Activity Type'] == 'Mountain Biking') |
           (df['Activity Type'] == 'Indoor Cycling')) &
           (df['Max. Speed (km/h)'] >= max_allowed_cycling_speed_in_kmh)
        )
    ]

    return df