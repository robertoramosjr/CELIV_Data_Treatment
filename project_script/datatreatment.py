import os.path
import numpy as np
from scipy.signal import savgol_filter
from scipy import integrate
import pandas as pd

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


def integrate_data(array_y, array_x):
    temp_list = []
    for key, value in enumerate(array_y):
        temp_list.append(
            integrate.simps(array_y[key], array_x[key], even='avg')
        )
    return temp_list


def smooth_current_noise(current_data_as_array):
    temp_list = []
    for key, values in enumerate(current_data_as_array):
        temp_list.append((savgol_filter(current_data_as_array[key], 60, 2).tolist()))
    return temp_list


def find_peaks(data_as_list):
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


def flatten_list_of_lists(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def mobility_calculus(data_frame_with_required_data):
    mobility = (
        data_frame_with_required_data['first term of mobility calculations (cm^2/s)'] /
        data_frame_with_required_data['ramp rates (V/s)']
        ) *\
        (
        (
            (1 / (6.2 * (1 + (0.002 * (
                data_frame_with_required_data['delta_j (A/m^2)'] /
                data_frame_with_required_data['j0 (A/m^2)']
                )
            )))) +
            (1 / (1 + (0.12 * (
                data_frame_with_required_data['delta_j (A/m^2)'] /
                data_frame_with_required_data['j0 (A/m^2)']
                )
            )))
        )
        ** 2
        )\
        .round(30)
    return mobility


def find_displacement_current(dark_celiv_current_results):
    displacement_current_values = pd.Series(
            dark_celiv_current_results.iloc[len(dark_celiv_current_results) - 1, x]
            for x in list(range(0, (len(dark_celiv_current_results.columns))))
        ) \
            .round(decimals=30)
    return displacement_current_values
