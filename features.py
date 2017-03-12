from tsfresh.examples import load_robot_execution_failures
from tsfresh.examples import download_robot_execution_failures
from tsfresh import select_features
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute
import pandas as pd
import numpy as np

def get_features(input_data, labels):

    used_records = input_data[0][1]

    time_series, target_classes = construct_tkfresh_input(used_records, labels)
    #download_robot_execution_failures()
    #time_series, Y = load_robot_execution_failures()

    print(time_series)

    extracted_features = extract_features(time_series, column_id='id', column_sort='time', column_value='value')
    impute(extracted_features)
    X = select_features(extracted_features, target_classes)
    print(X)

    Y = pd.Series(labels)
    return X, Y

def construct_tkfresh_input(file_record, labels):

    label_mapping = {}
    label_id = 0
    for item in labels:
        if label_id > 0 and item in label_mapping:
            continue
        else:
            label_id += 1
            label_mapping[item] = label_id
    print(label_mapping)

    id_to_target = []
    df_rows = []

    cur_id = 0
    for trace in file_record:
        id_to_target.append(label_mapping[labels[cur_id]])
        for point in trace:
            time_stamp = point[1]
            value = point[0]
            df_rows.append([cur_id, time_stamp, value])
        cur_id += 1

    df = pd.DataFrame(df_rows, columns=['id', 'time', 'value'])
    #y = pd.Series(id_to_target)
    y = np.array(id_to_target)
    return df, y