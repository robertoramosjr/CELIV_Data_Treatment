import os.path
import numpy as np
from scipy.signal import savgol_filter


def separate_odd_columns(data_frame):
    return data_frame.iloc[:, 1::2]


def separate_even_columns(data_frame):
    return data_frame.iloc[:, ::2]


def is_valid_file(file_path):
    return True if file_path != "" and os.path.exists(file_path) else False


def is_bigger_data_frame(data_frame_1, data_frame_2):
    return len(data_frame_1) > len(data_frame_2)


def equalize_data_frame_rows(data_frame_1, data_frame_2):
    return data_frame_1.loc[0:len(data_frame_2)-1, :]


def smooth(array):
    temp_list = []
    for key, values in enumerate(array):
        temp_list.append((savgol_filter(array[key], 55, 2).tolist()))
    return temp_list


def find_the_peaks(data_as_list):
    temp_list = []
    for key, value in enumerate(data_as_list):
        temp_list.append(data_as_list[key].max())
    return temp_list


def find_peak_index(array, peak_list):
    temp_list = []
    for key, values in enumerate(array):
        temp_list.append(np.where(array[key] == peak_list[key]))
    return temp_list


def find_time_max(array, index_list):
    temp_list = []
    for key, value in enumerate(array):
        temp_list.append(array[key][index_list[key]].tolist())
    return temp_list


def flatten(t):
    return [item for sublist in t for item in sublist]
