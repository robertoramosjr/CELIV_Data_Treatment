import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate
import ask
import datatreatment as dt
import constantvalues as cv


def message_invalid_path():
    return print("Arquivo inválido ou inexistente \n")


def sanitize_data_frames():
    global odd_columns_subtracted, time_photo_celiv_ramp_time
    if dt.is_bigger_data_frame(
            time_photo_celiv_ramp_time,
            odd_columns_subtracted
    ):
        time_photo_celiv_ramp_time = dt.equalize_data_frame_rows(
            time_photo_celiv_ramp_time,
            odd_columns_subtracted
        )
        return
    odd_columns_subtracted = dt.equalize_data_frame_rows(
        odd_columns_subtracted,
        time_photo_celiv_ramp_time
    )


def integrate_data():
    global time_photo_celiv_ramp_time_transposed, odd_columns_subtracted_transposed_in_arrays
    integrated_values = []
    for key, value in enumerate(odd_columns_subtracted_transposed_in_arrays):
        integrated_values.append(
            integrate.simps(
                odd_columns_subtracted_transposed_in_arrays[key],
                time_photo_celiv_ramp_time_transposed[key],
                even='avg'
            )
        )
    return integrated_values


# device_thickness = ask.device_thickness()
# device_area = ask.device_area()
charge_density_calculation_constant = cv.current_correction_factor * cv.charge_density_correction_factor \
                                      / (cv.electron_charge * cv.device_area * cv.device_thickness)

# path_dark = ask.file_path("dark-CELIV")
#
# while not is_valid_file(path_dark):
#     message_invalid_path()
#     path_dark = ask.file_path("dark-CELIV")
#
current_dark_celiv_ramp_time = dt.separate_odd_columns(
    pd.read_table(
        "C:/Users/robee/Desktop/2-dark-celiv-current-celiv-only-alterado.txt",
        sep='\t',
        header=None
    )
)\
    .abs()\
    .dropna()

# path_photo = ask.file_path("photo_celiv")

# while not is_valid_file(path_photo):
#     message_invalid_path()
#     path_photo = ask.file_path("photo-celiv")

current_photo_celiv_ramp_time = dt.separate_odd_columns(
    pd.read_table(
        "C:/Users/robee/Desktop/3-photo-celiv-basic-current-celiv-only-alterado.txt",
        sep='\t',
        header=None
    )
)\
    .abs()

time_photo_celiv_ramp_time = dt.separate_even_columns(
    pd.read_table(
        "C:/Users/robee/Desktop/3-photo-celiv-basic-current-celiv-only-alterado.txt",
        sep='\t',
        header=None
    )
)

odd_columns_subtracted = current_photo_celiv_ramp_time\
    .subtract(current_dark_celiv_ramp_time)\
    .dropna()

sanitize_data_frames()

data_ramp_time = pd.concat(
    [time_photo_celiv_ramp_time, odd_columns_subtracted],
    axis=1
)\
    .sort_index(axis=1)

# data_ramp_time.to_excel("C:/Users/robee/Desktop/data_ramp_time.xlsx")

# data_ramp_time.to_csv(ask.file_name(), sep='\t') #line commented to run tests

data_ramp_time_transposed_in_arrays = data_ramp_time.transpose().to_numpy()

time_photo_celiv_ramp_time_transposed = time_photo_celiv_ramp_time.transpose().to_numpy()

odd_columns_subtracted_transposed_in_arrays = odd_columns_subtracted.transpose().to_numpy()

integration_results = integrate_data()

# pd.DataFrame(integrate_data()).to_csv("C:/Users/robee/Desktop/integral_values.txt")

density_of_carriers = [element * charge_density_calculation_constant for element in integration_results]

pd.DataFrame(density_of_carriers).to_csv(
    "C:/Users/robee/Desktop/density_of_carriers_test.txt",
    sep='\t',
    decimal=','
)
