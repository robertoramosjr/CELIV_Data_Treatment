import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate
import ask


def separate_even_columns(data_frame):
    return data_frame.iloc[:, [i for i in range(len(data_frame.columns)) if i % 2 == 1]]


def separate_odd_columns(data_frame):
    return data_frame.iloc[:, [i for i in range(len(data_frame.columns)) if i % 2 == 0]]


def is_valid_file(file_path):
    return True if file_path != "" and os.path.exists(file_path) else False


def message_invalid_path():
    return print("Arquivo inválido ou inexistente \n")


def is_bigger_data_frame(data_frame_1, data_frame_2):
    return len(data_frame_1) > len(data_frame_2)


def equalize_data_frame_rows(data_frame_1, data_frame_2):
    return data_frame_1.loc[0:len(data_frame_2)-1, :]


def sanitize_data_frames():
    global even_columns_subtracted, time_photo_celiv_ramp_time
    if is_bigger_data_frame(time_photo_celiv_ramp_time, even_columns_subtracted):
        time_photo_celiv_ramp_time = equalize_data_frame_rows(time_photo_celiv_ramp_time, even_columns_subtracted)
        return
    even_columns_subtracted = equalize_data_frame_rows(even_columns_subtracted, time_photo_celiv_ramp_time)


def integrate_data():
    global time_photo_celiv_ramp_time_transposed, even_columns_subtracted_transposed_in_arrays
    integrated_values = []
    for key, value in enumerate(even_columns_subtracted_transposed_in_arrays):
        integrated_values.append(integrate.simps(even_columns_subtracted_transposed_in_arrays[key],
                                                 time_photo_celiv_ramp_time_transposed[key], even='avg'))
    return integrated_values


# device_thickness = ask.ask_device_thickness()

# device_area = ask.ask_device_area()

electron_charge = 1.6*10**(-19)

device_area = 1.4*10**(-5)

device_thickness = 600*10**(-9)

current_correction_factor = 1*10**(-9)

charge_density_correction_factor = 1*10**(-6)

charge_density_calculation_constant = current_correction_factor * charge_density_correction_factor \
                                      / (electron_charge * device_area * device_thickness)

# path_dark = ask_file_path("dark-CELIV")
#
# while not is_valid_file(path_dark):
#     message_invalid_path()
#     path_dark = ask.ask_file_path("dark-CELIV")
#
current_dark_celiv_ramp_time = separate_even_columns(pd.read_table("C:/Users/robee/Desktop/"
                                                                   "2-dark-celiv-current-celiv-only-alterado.txt",
                                                                   sep='\t', header=None))\
    .abs()\
    .dropna()

# path_photo = ask.ask_file_path("photo_celiv")

# while not is_valid_file(path_photo):
#     message_invalid_path()
#     path_photo = ask.ask_file_path("photo-celiv")

current_photo_celiv_ramp_time = (separate_even_columns(
    pd.read_table("C:/Users/robee/Desktop/3-photo-celiv-basic-current-celiv-only-alterado.txt",
                  sep='\t', header=None)))\
    .abs()

time_photo_celiv_ramp_time = separate_odd_columns(
    pd.read_table("C:/Users/robee/Desktop/3-photo-celiv-basic-current-celiv-only-alterado.txt",
                  sep='\t', header=None))

even_columns_subtracted = current_photo_celiv_ramp_time\
    .subtract(current_dark_celiv_ramp_time)\
    .dropna()

sanitize_data_frames()

data_ramp_time = pd.concat([time_photo_celiv_ramp_time, even_columns_subtracted],
                           axis=1).sort_index(axis=1)

# data_ramp_time.to_excel("C:/Users/robee/Desktop/data_ramp_time.xlsx")

# data_ramp_time.to_csv(ask.ask_file_name(), sep='\t') #line commented to run tests

data_ramp_time_transposed_in_arrays = data_ramp_time.transpose().to_numpy()

time_photo_celiv_ramp_time_transposed = time_photo_celiv_ramp_time.transpose().to_numpy()

even_columns_subtracted_transposed_in_arrays = even_columns_subtracted.transpose().to_numpy()

integration_results = integrate_data()

# pd.DataFrame(integrate_data()).to_csv("C:/Users/robee/Desktop/integral_values.txt")

density_of_carriers = [element * charge_density_calculation_constant for element in integration_results]

pd.DataFrame(density_of_carriers).to_csv("C:/Users/robee/Desktop/density_of_carriers.txt", sep='\t', decimal=',')


