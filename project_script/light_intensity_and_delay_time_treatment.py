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
#     ask.file_path("light intensity")

# DEVICE_THICKNESS = ask.device_thickness()
# DEVICE_AREA = ask.device_area()
# ramp_rate = ask.scan_rate()
meas_number = ask.meas_number()
ramp_rate = 60000
CHARGE_DENSITY_CALCULATION = cv.CTTS_PRODUCT / (cv.DEVICE_AREA * cv.DEVICE_THICKNESS)
INTENSITY_NUMBER = 10
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

results = pd.DataFrame([(cv.INTENSITIES * meas_number), density_of_carriers_li])\
    .transpose()\
    .set_axis(['Light Intensity (mW/cm2)', 'n'], axis=1)

for k, v in enumerate(current_subtracted_as_array):
    plt.plot(time_as_array[k], current_subtracted_as_array[k])

current_subtracted_smoothed = np.array(dt.smooth_current_noise(current_subtracted_as_array))

current_peaks_light_intensity = dt.find_peaks(current_subtracted_smoothed)

results['current peak'] = pd.DataFrame([current_peaks_light_intensity]).transpose()

peaks_indexes = dt.find_peak_index(current_subtracted_smoothed, current_peaks_light_intensity)

time_max_light_intensity = dt.flatten_list_of_lists(dt.find_time_max(time_as_array, peaks_indexes))

results['peak time'] = pd.DataFrame([time_max_light_intensity]).transpose()

results['delta_j (A/m^2)'] = results['current peak'] * cv.CURRENT_CORRECTION_FACTOR / cv.DEVICE_AREA

results['first term of mobility calculations (cm^2/s)'] = (
        ((cv.DEVICE_THICKNESS ** 2) * cv.SQR_METER_SQR_CENTIMETER_CONVERSION) /
        (2 * results['peak time'] ** 2 * cv.SQUARED_TIME_CORRECTION_FACTOR)
    )\
    .round(decimals=30)

displacement_current = dt.find_displacement_current(current_dark_celiv)

results['j0 (A/m^2)'] = displacement_current * cv.CURRENT_CORRECTION_FACTOR / cv.DEVICE_AREA

results['ramp rates (V/s)'] = pd.Series([ramp_rate] * meas_number * INTENSITY_NUMBER)\
    .sort_values(ascending=True, ignore_index=True)

results['mobility (cm^2 / Vs)'] = dt.mobility_calculus(results)

for k, v in enumerate(current_subtracted_smoothed):
    plt.plot(time_as_array[k], current_subtracted_smoothed[k])
for k, v in enumerate(peaks_indexes):
    plt.scatter(time_max_light_intensity[k], current_peaks_light_intensity[k])
plt.show()

results_intensity = pd.DataFrame(
        [
            results['Light Intensity (mW/cm2)'],
            results['peak time'],
            results['delta_j (A/m^2)'],
            results['j0 (A/m^2)'],
            results['mobility (cm^2 / Vs)'],
            results['n']
        ]
    ).transpose()

results_intensity.to_csv(ask.file_name('intensity'), sep='\t', index=False)
