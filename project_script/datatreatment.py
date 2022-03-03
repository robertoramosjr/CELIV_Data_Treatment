import os.path


def separate_even_columns(data_frame):
    return data_frame.iloc[:, [i for i in range(len(data_frame.columns)) if i % 2 == 1]]


def separate_odd_columns(data_frame):
    return data_frame.iloc[:, [i for i in range(len(data_frame.columns)) if i % 2 == 0]]


def is_valid_file(file_path):
    return True if file_path != "" and os.path.exists(file_path) else False


def is_bigger_data_frame(data_frame_1, data_frame_2):
    return len(data_frame_1) > len(data_frame_2)


def equalize_data_frame_rows(data_frame_1, data_frame_2):
    return data_frame_1.loc[0:len(data_frame_2)-1, :]
