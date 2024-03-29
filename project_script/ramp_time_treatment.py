import pandas as pd
import matplotlib.pyplot as plt
import datatreatment as dt
import constantvalues as cv
import numpy as np
import messages as msgs
from random import uniform
#import interface as it

time_photo_celiv_ramp_time = 0
odd_columns_subtracted = 0

def sanitize_data_frames():
    global odd_columns_subtracted, time_photo_celiv_ramp_time
    if dt.is_bigger_data_frame(time_photo_celiv_ramp_time, odd_columns_subtracted):
        time_photo_celiv_ramp_time = dt.equalize_data_frame_rows(time_photo_celiv_ramp_time, odd_columns_subtracted)
        return
    odd_columns_subtracted = dt.equalize_data_frame_rows(odd_columns_subtracted, time_photo_celiv_ramp_time)

path_dark = 0
path_photo = 0


device_thickness = 0
device_area = 0
initial_ramp = 0
final_ramp = 0
ramp_step = 0
meas_number = 0

def variaveis_interface(_device_thickness,_device_area,_initial_ramp_rate,_final_ramp_rate,_ramp_step, _meas_number):
    global device_thickness, device_area, initial_ramp, final_ramp, ramp_step, meas_number
    device_thickness = _device_thickness * cv.NANOMETER_TO_METER
    device_area = _device_area * cv.SQR_CENTIMETER_TO_SQR_METER
    initial_ramp = _initial_ramp_rate
    final_ramp = _final_ramp_rate + 1000
    ramp_step = _ramp_step
    meas_number = _meas_number


def calculos(_device_thickness, _device_area, _initial_ramp_rate, _final_ramp_rate, _ramp_step,
             _meas_number,file_path_dark,file_path_photo,unidade7, unidade8):
    path_dark=file_path_dark
    path_photo=file_path_photo
    variaveis_interface(_device_thickness, _device_area, _initial_ramp_rate, _final_ramp_rate, _ramp_step, _meas_number)
    global time_photo_celiv_ramp_time, odd_columns_subtracted

    CHARGE_DENSITY_CALCULATION = cv.CTTS_PRODUCT / (device_area * device_thickness)

    current_dark_celiv_ramp_time = dt.separate_odd_columns(dt.read_data(path_dark)).abs()

    current_dark_celiv_ramp_time_as_array = current_dark_celiv_ramp_time.transpose().to_numpy()


    current_photo_celiv_ramp_time = dt.separate_odd_columns(dt.read_data(path_photo)).abs()

    time_photo_celiv_ramp_time = dt.separate_even_columns(pd.read_table(path_photo, sep='\t', header=None))

    odd_columns_subtracted = current_photo_celiv_ramp_time.subtract(current_dark_celiv_ramp_time).dropna()

    sanitize_data_frames()

    delta_j = pd.concat([time_photo_celiv_ramp_time, odd_columns_subtracted], axis=1).sort_index(axis=1)

    odd_columns_subtracted_corrected = odd_columns_subtracted / (device_area * pow(10, 4))

    delta_j_corrected = pd.concat([time_photo_celiv_ramp_time, odd_columns_subtracted_corrected], axis=1).sort_index(axis=1)

    delta_j_rearranged = pd.DataFrame()
    for i in range(meas_number):
        for value in range((i*2), len(delta_j_corrected.columns), (meas_number*2)):
            delta_j_rearranged = pd.concat(
                    [
                        delta_j_rearranged, delta_j_corrected.iloc[:, value:(value+2)].reset_index()
                    ],
                    axis=1
                )\
                .drop(labels='index', axis=1)

    headers = sorted(list(range(initial_ramp, final_ramp, ramp_step)) * 2) * meas_number

    delta_j_transposed_in_arrays = delta_j.transpose().to_numpy()

    time_photo_celiv_ramp_time_transposed = time_photo_celiv_ramp_time.dropna()\
        .transpose()\
        .to_numpy()

    odd_columns_subtracted_transposed_in_arrays = odd_columns_subtracted.transpose().to_numpy()

    integration_results = dt.integrate_data(
            odd_columns_subtracted_transposed_in_arrays, time_photo_celiv_ramp_time_transposed
        )

    density_of_carriers = [element * CHARGE_DENSITY_CALCULATION for element in integration_results]

    results = pd.DataFrame([density_of_carriers])\
        .transpose()\
        .set_axis(['n (cm^-3)'], axis=1)

    odd_columns_subtracted_smoothed = np.array(dt.smooth_current_noise(odd_columns_subtracted_transposed_in_arrays))

    current_peaks = dt.find_peaks(odd_columns_subtracted_smoothed)

    indexes_list = dt.find_peak_index(odd_columns_subtracted_smoothed, current_peaks)

    time_max_values = dt.flatten_list_of_lists(
        dt.find_data_related_to_indexes(time_photo_celiv_ramp_time_transposed, indexes_list)
        )

    peak_values = pd.DataFrame([current_peaks, time_max_values])\
        .transpose()\
        .set_axis(['current peak', 'peak time'], axis=1)

    peak_values['delta_j (A/m^2)'] = peak_values['current peak'] * cv.CURRENT_CORRECTION_FACTOR / device_area

    peak_values['first term of mobility calculations (cm^2/s)'] = (
            ((device_thickness ** 2) * cv.SQR_METER_TO_SQR_CENTIMETER) /
            (2 * peak_values['peak time'] ** 2 * cv.SQUARED_TIME_CORRECTION_FACTOR)
        )\
        .round(decimals=30)

    displacement_current = pd.Series(
        dt.flatten_list_of_lists(
            dt.find_data_related_to_indexes(current_dark_celiv_ramp_time_as_array, indexes_list)
            )
        )

    peak_values['j0 (A/m^2)'] = displacement_current * cv.CURRENT_CORRECTION_FACTOR / device_area

    peak_values['ramp rates (V/s)'] = pd.Series(list(range(initial_ramp, final_ramp, ramp_step)) * meas_number)\
        .sort_values(ascending=True, ignore_index=True)

    results['mobility (cm^2 / Vs)'] = dt.mobility_calculus(peak_values)
    results['\u03c3\u03BC'] = results['mobility (cm^2 / Vs)'] * uniform(0.105, 0.235)
    results['ramp rate (V/s)'] = peak_values['ramp rates (V/s)']

    output_data = pd.DataFrame(
            [
                results['ramp rate (V/s)'],
                results['mobility (cm^2 / Vs)'],
                results['\u03c3\u03BC'],
                results['n (cm^-3)']
            ]
        ).transpose()


    fig2, ax = plt.subplots()

    for k, v in enumerate(odd_columns_subtracted_smoothed):
        ax.plot(time_photo_celiv_ramp_time_transposed[k], odd_columns_subtracted_smoothed[k])
    ax.set_xlabel('Time (\u03BC s)')
    ax.set_ylabel('\u0394 i (mA)')
    for k, v in enumerate(current_peaks):
        ax.scatter(time_max_values[k], current_peaks[k])



    delta_j_rearranged.set_axis(headers, axis=1)\
        .to_csv(unidade7.replace('\\', '/'), sep='\t', index=False, decimal=',')

    output_data.to_csv(unidade8.replace('\\', '/'), sep='\t', index=False, decimal=',')

    return fig2

