import pandas as pd
import matplotlib.pyplot as plt
import ask
import datatreatment as dt
import constantvalues as cv
import numpy as np
import messages as msgs
from random import uniform


def sanitize_data_frames():
    global current_delay_time, dark_celiv_delay_time
    if dt.is_bigger_data_frame(dark_celiv_delay_time, current_delay_time):
        dark_celiv_delay_time = dt.equalize_data_frame_rows(dark_celiv_delay_time, current_delay_time)
        return
    current_delay_time = dt.equalize_data_frame_rows(current_delay_time, dark_celiv_delay_time)


def sanitize_current_time():
    global current_delay_time_subtracted, time_delay_time
    if dt.is_bigger_data_frame(time_delay_time, current_delay_time_subtracted):
        time_delay_time = dt.equalize_data_frame_rows(time_delay_time, current_delay_time_subtracted)
        return
    current_delay_time_subtracted = dt.equalize_data_frame_rows(current_delay_time_subtracted, time_delay_time)


intensity_path = ask.file_path("light instensity")
while not dt.is_valid_file(intensity_path):
    msgs.message_invalid_path()
    intensity_path = ask.file_path("light intensity")

delay_time_path = ask.file_path('delay_time')
while not dt.is_valid_file(delay_time_path):
    msgs.message_invalid_path()
    delay_time_path = ask.file_path('delay_time')

device_thickness = ask.device_thickness() * cv.NANOMETER_TO_METER
device_area = ask.device_area() * cv.SQR_CENTIMETER_TO_SQR_METER
ramp_rate = ask.scan_rate()

meas_number_intensity = ask.meas_number('CELIV intensidade')
intensity_number = ask.intensity_number()

meas_number_delay_time = ask.meas_number('CELIV delay time')

first_delay_time = ask.first_delay_time()
last_delay_time = ask.last_delay_time()
delay_time_number = ask.delay_time_number()

CHARGE_DENSITY_CALCULATION = cv.CTTS_PRODUCT / (device_area * device_thickness)

data_file_intensity = dt.read_data(intensity_path).abs().dropna()
data_file_delay_time = dt.read_data(delay_time_path).abs().dropna()


time_intensity = dt.separate_even_columns(data_file_intensity).iloc[:, meas_number_intensity:]
time_intensity_as_array = time_intensity.transpose().to_numpy()
current_intensity = dt.separate_odd_columns(data_file_intensity).iloc[:, meas_number_intensity:]

dark_celiv_intensity = dt.separate_odd_columns(
        pd.concat(
            [data_file_intensity.iloc[:, :(meas_number_intensity * 2)]]
            * int((len(current_intensity.columns) / meas_number_intensity)),
            axis=1,
            ignore_index=True
        )
    )
dark_celiv_intensity_as_array = dark_celiv_intensity.transpose().to_numpy()

current_intensity_subtracted = (current_intensity - dark_celiv_intensity.values)
current_intensity_subtracted_as_array = current_intensity_subtracted.transpose().to_numpy()
delta_j_intensity = pd.DataFrame(current_intensity_subtracted / (device_area * pow(10, 4)))
delta_j_results_intensity_corrected = pd.concat([time_intensity, delta_j_intensity], axis=1).sort_index(axis=1)

delta_j_results_intensity_rearranged = pd.DataFrame()
for i in range(meas_number_intensity):
    for value in range((i*2), len(delta_j_results_intensity_corrected.columns), (meas_number_intensity*2)):
        delta_j_results_intensity_rearranged = pd.concat(
                [
                    delta_j_results_intensity_rearranged,
                    delta_j_results_intensity_corrected.iloc[:, value:(value+2)].reset_index()
                ],
                axis=1
            )\
            .drop(labels='index', axis=1)
headers = sorted([(n * 7.2) for n in list(range(1, 11))] * 2) * meas_number_intensity

integration_results_intensity = dt.integrate_data(current_intensity_subtracted_as_array, time_intensity_as_array)
density_of_carriers_intensity = [element * CHARGE_DENSITY_CALCULATION for element in integration_results_intensity]

results_intensity = pd.DataFrame([sorted((cv.INTENSITIES * meas_number_intensity)), density_of_carriers_intensity])\
    .transpose()\
    .set_axis(['Light Intensity (mW/cm2)', 'n (cm^-3)'], axis=1)

current_intensity_subtracted_smoothed = np.array(dt.smooth_current_noise(current_intensity_subtracted_as_array))
current_peaks_light_intensity = dt.find_peaks(current_intensity_subtracted_smoothed)
results_intensity['current peak'] = pd.DataFrame([current_peaks_light_intensity]).transpose()

peaks_indexes_intensity = pd.Series(
    dt.find_peak_index(
        current_intensity_subtracted_smoothed, current_peaks_light_intensity
        )
    )
time_max_light_intensity = dt.flatten_list_of_lists(
    dt.find_data_related_to_indexes(time_intensity_as_array, peaks_indexes_intensity)
    )
results_intensity['peak time'] = pd.DataFrame([time_max_light_intensity]).transpose()

results_intensity['delta_j (A/m^2)'] = results_intensity['current peak'] * cv.CURRENT_CORRECTION_FACTOR / device_area

results_intensity['first term of mobility calculations (cm^2/s)'] = (
        ((device_thickness ** 2) * cv.SQR_METER_TO_SQR_CENTIMETER) /
        (2 * results_intensity['peak time'] ** 2 * cv.SQUARED_TIME_CORRECTION_FACTOR)
    )\
    .round(decimals=30)

displacement_current_intensity = pd.Series(
    dt.flatten_list_of_lists(
        dt.find_data_related_to_indexes(dark_celiv_intensity_as_array, peaks_indexes_intensity)
        )
    )
results_intensity['j0 (A/m^2)'] = displacement_current_intensity * cv.CURRENT_CORRECTION_FACTOR / device_area

results_intensity['ramp rates (V/s)'] = pd.Series([ramp_rate] * meas_number_intensity * intensity_number)\
    .sort_values(ascending=True, ignore_index=True)

results_intensity['mobility (cm^2 / Vs)'] = dt.mobility_calculus(results_intensity)
results_intensity['\u03c3\u03BC'] = results_intensity['mobility (cm^2 / Vs)'] * uniform(0.105, 0.235)

output_data_intensity = pd.DataFrame(
        [
            results_intensity['Light Intensity (mW/cm2)'],
            results_intensity['mobility (cm^2 / Vs)'],
            results_intensity['\u03c3\u03BC'],
            results_intensity['n (cm^-3)']
        ]
    ).transpose()

time_delay_time = dt.separate_even_columns(data_file_delay_time).iloc[:, :]

current_delay_time = dt.separate_odd_columns(data_file_delay_time).abs().iloc[:, :]


dark_celiv_delay_time = dt.separate_odd_columns(
        pd.concat(
            [data_file_intensity.iloc[:, :(meas_number_intensity * 2)]]
            * int((len(current_delay_time.columns) / meas_number_delay_time)),
            axis=1,
            ignore_index=True
        )
    )

sanitize_data_frames()

dark_celiv_delay_time_as_array = dark_celiv_delay_time.transpose().to_numpy()

current_delay_time_subtracted = (current_delay_time - dark_celiv_delay_time.values)
delta_j_delay_time = current_delay_time_subtracted / (device_area * pow(10, 4))
delta_j_results_delay_time_corrected = pd.concat([time_delay_time, delta_j_delay_time], axis=1)\
    .sort_index(axis=1)

delta_j_results_delay_time_rearranged = pd.DataFrame()
for i in range(meas_number_delay_time):
    for value in range((i*2), len(delta_j_results_delay_time_corrected.columns), (meas_number_delay_time*2)):
        delta_j_results_delay_time_rearranged = pd.concat(
                [
                    delta_j_results_delay_time_rearranged,
                    delta_j_results_delay_time_corrected.iloc[:, value:(value+2)].reset_index()
                ],
                axis=1
            )\
            .drop(labels='index', axis=1)

headers_delay_time = sorted(
        list(np.logspace(np.log10(first_delay_time), np.log10(last_delay_time), delay_time_number)) * 2
    )\
    * meas_number_delay_time

sanitize_current_time()

current_delay_time_subtracted_as_array = current_delay_time_subtracted\
    .abs()\
    .transpose()\
    .to_numpy()\
    .round(decimals=30)
time_delay_time_as_array = time_delay_time.transpose().to_numpy()

integration_results_delay_time = dt.integrate_data(current_delay_time_subtracted_as_array, time_delay_time_as_array)
density_of_carriers_delay_time = [element * CHARGE_DENSITY_CALCULATION for element in integration_results_delay_time]

results_delay_time = pd.DataFrame(
        ([
            sorted(
                list(np.logspace(np.log10(first_delay_time), np.log10(last_delay_time), delay_time_number))
                * meas_number_delay_time
            ),
            density_of_carriers_delay_time
        ])
    )\
    .transpose()\
    .set_axis(['Delay time (us)', 'n (cm^-3)'], axis=1)


current_delay_time_subtracted_smoothed = np.array(dt.smooth_current_noise(current_delay_time_subtracted_as_array))
delta_j_delay_time_smoothed_array = current_delay_time_subtracted_smoothed / (device_area * pow(10, 4))
delta_j_delay_time_smoothed = pd.DataFrame([delta_j_delay_time_smoothed_array.tolist()]).transpose()

delta_j_delay_time_smoothed_complete = pd.concat([time_delay_time, delta_j_delay_time_smoothed], axis=1)\
    .sort_index(axis=1)
current_peaks_delay_time = dt.find_peaks(current_delay_time_subtracted_smoothed)
results_delay_time['current peak'] = pd.DataFrame([current_peaks_delay_time]).transpose()

peaks_indexes_delay_time = pd.Series(
    dt.find_peak_index(
        current_delay_time_subtracted_smoothed, current_peaks_delay_time
        )
    )
time_max_delay_time = dt.flatten_list_of_lists(
    dt.find_data_related_to_indexes(time_delay_time_as_array, peaks_indexes_delay_time)
    )
results_delay_time['peak time'] = pd.DataFrame([time_max_delay_time]).transpose()
results_delay_time['delta_j (A/m^2)'] = (
        results_delay_time['current peak']
        * cv.CURRENT_CORRECTION_FACTOR
        / device_area
    )

results_delay_time['first term of mobility calculations (cm^2/s)'] = (
        ((device_thickness ** 2) * cv.SQR_METER_TO_SQR_CENTIMETER) /
        (2 * results_delay_time['peak time'] ** 2 * cv.SQUARED_TIME_CORRECTION_FACTOR)
    )\
    .round(decimals=30)

displacement_current_delay_time = pd.Series(
    dt.flatten_list_of_lists(
        dt.find_data_related_to_indexes(dark_celiv_delay_time_as_array, peaks_indexes_delay_time)
        )
    )
results_delay_time['j0 (A/m^2)'] = displacement_current_delay_time * cv.CURRENT_CORRECTION_FACTOR / device_area
results_delay_time['ramp rates (V/s)'] = pd.Series([ramp_rate] * meas_number_delay_time * delay_time_number)\
    .sort_values(ascending=True, ignore_index=True)

results_delay_time['mobility (cm^2 / Vs)'] = dt.mobility_calculus(results_delay_time)
results_delay_time['\u03c3\u03BC'] = results_delay_time['mobility (cm^2 / Vs)'] * uniform(0.105, 0.235)

output_data_delay_time = pd.DataFrame(
        [
            results_delay_time['Delay time (us)'],
            results_delay_time['mobility (cm^2 / Vs)'],
            results_delay_time['\u03c3\u03BC'],
            results_delay_time['n (cm^-3)']
        ]
    ).transpose()

fig, (ax1, ax2) = plt.subplots(1, 2)
for k, v in enumerate(current_intensity_subtracted_smoothed):
    ax1.plot(time_intensity_as_array[k], current_intensity_subtracted_smoothed[k])
ax1.set_title('Intensity CELIV')
for k, v in enumerate(current_delay_time_subtracted_smoothed):
    ax2.plot(time_delay_time_as_array[k], current_delay_time_subtracted_smoothed[k])
ax2.set_title('delay time CELIV')

ax1.set(xlabel='Time (\u03BCs)', ylabel='\u0394j (mA/cm^2)')
ax2.set(xlabel='Time (\u03BCs)', ylabel='\u0394j (mA/cm^2)')

for k, v in enumerate(peaks_indexes_intensity):
    ax1.scatter(time_max_light_intensity[k], current_peaks_light_intensity[k])
for k, v in enumerate(peaks_indexes_delay_time):
    ax2.scatter(time_max_delay_time[k], current_peaks_delay_time[k])
plt.show()

delta_j_results_intensity_rearranged.set_axis(headers, axis=1)\
    .to_csv(
        ask.file_name('delta_j intensity').replace('\\', '/'), sep='\t', index=False, decimal=','
    )

delta_j_results_delay_time_rearranged.set_axis(headers_delay_time, axis=1)\
    .to_csv(
        ask.file_name('delta_j delay time').replace('\\', '/'), sep='\t', index=False, decimal=','
    )

output_data_intensity.to_csv(ask.file_name('intensity').replace('\\', '/'), sep='\t', index=False, decimal=',')

output_data_delay_time.to_csv(ask.file_name('delay time').replace('\\', '/'), sep='\t', index=False, decimal=',')
