import pandas as pd
import matplotlib.pyplot as plt
import ask
import datatreatment as dt
import constantvalues as cv
import numpy as np
import messages as msgs


# data_path = ask.file_path("light instensity or delay time")
# while not dt.is_valid_file(data_path):
#     msgs.message_invalid_path()
#     ask.file_path("li_or_delay_time")

# DEVICE_THICKNESS = ask.device_thickness()
# DEVICE_AREA = ask.device_area()
CHARGE_DENSITY_CALCULATION = cv.CTTS_PRODUCT / (cv.DEVICE_AREA * cv.DEVICE_THICKNESS)

# data_file = pd.read_table(data_path, sep='\t', header=None).abs().dropna()
data_file_intensity = pd.read_table(
    "C:/Users/robee/Desktop/4-photo-celiv-intensity-device1_cell1-current-celiv-only-alterado.txt",
    sep='\t',
    header=None)\
    .abs()\
    .dropna()\
    .iloc[:776, :]

time = dt.separate_even_columns(data_file_intensity).iloc[:, 1:]
time_as_array = time.transpose().to_numpy()

current = dt.separate_odd_columns(data_file_intensity).iloc[:, 1:]

current_dark_celiv = pd.concat([data_file_intensity.iloc[:, 1:2]] * len(current.columns), axis=1, ignore_index=True)

current_subtracted = current - current_dark_celiv.values
current_subtracted_as_array = current_subtracted.transpose().to_numpy()

integration_results_li = dt.integrate_data(current_subtracted_as_array, time_as_array)

density_of_carriers_li = [element * CHARGE_DENSITY_CALCULATION for element in integration_results_li]

results = pd.DataFrame([cv.INTENSITIES, density_of_carriers_li])\
    .transpose()\
    .set_axis(['Light Intensity', 'n'], axis=1)

for k, v in enumerate(current_subtracted_as_array):
    plt.plot(time_as_array[k], current_subtracted_as_array[k])

current_subtracted_smoothed = np.array(dt.smooth_current_noise(current_subtracted_as_array))

current_peaks_light_intensity = dt.find_peaks(current_subtracted_smoothed)

results['current peak'] = pd.DataFrame([current_peaks_light_intensity]).transpose()

peaks_indexes = dt.find_peak_index(current_subtracted_smoothed, current_peaks_light_intensity)

time_max_light_intensity = dt.flatten_list_of_lists(dt.find_time_max(time_as_array, peaks_indexes))

results['time of max.'] = pd.DataFrame([time_max_light_intensity]).transpose()

for k, v in enumerate(current_subtracted_smoothed):
    plt.plot(time_as_array[k], current_subtracted_smoothed[k])
for k, v in enumerate(peaks_indexes):
    plt.scatter(time_max_light_intensity[k], current_peaks_light_intensity[k])
plt.show()

results.to_csv(ask.file_name(), sep='\t', index=False)
