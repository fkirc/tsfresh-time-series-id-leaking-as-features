import os, glob

def parse_input():
    
    print('Parse input files...')

    session_dir = 'binary_test'
    file_endings = '*.txt'

    # Top level cells (containing all files)
    input_data = []
    label_names = []

    first_file = True
    for file in glob.glob(os.path.join(session_dir, file_endings)):
        print(file)

        # Mid level cells(containing all the content of a file)
        values = []
        line_cnt = 0

        with open(file) as f:
            for line in f:

                # Low level cells(contain recorded traces)
                line_token = line.split(',')
                record_values = []

                number_of_data_points = len(line_token) - 2 # skip the label name at the last position
                for entry_cnt in range(0, number_of_data_points):

                    entry = line_token[entry_cnt].split('|')
                    value = int(entry[0]) # actual value
                    time_stamp = int(entry[1]) # relative time stamp
                    record_values.append([value, time_stamp])

                current_label = line_token[number_of_data_points]
                if first_file:
                    label_names.append(current_label)
                else:
                    if current_label != label_names[line_cnt]:
                        error_message = ('label name line mismatch - input files do not fit together')
                        raise ValueError(error_message)

                values.append(record_values)

                line_cnt += 1

            input_data.append([str(file), values])

        first_file = False

    #print(input_data)
    #print(label_names)
    return input_data, label_names
