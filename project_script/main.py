import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate


def separate_even_columns(data_frame):
    return data_frame.iloc[:, [i for i in range(len(data_frame.columns)) if i % 2 == 1]]


def separate_odd_columns(data_frame):
    return data_frame.iloc[:, [i for i in range(len(data_frame.columns)) if i % 2 == 0]]


def is_valid_file(file_path):
    return True if file_path != "" and os.path.exists(file_path) else False


def ask_file_path(measurement_name):
    return input(f"Insira o caminho do arquivo do {measurement_name} ramptime \n")


def message_invalid_path():
    return print("Arquivo inválido ou inexistente \n")


def ask_file_name():
    return input("Insira o nome do arquivo para salvar \n")


def ask_x_axys():
    return input('Insira o cabeçalho do eixo x a ser considerado para o plote \n')


def ask_y_axys():
    return input('Insira o cabeçalho do eixo y a ser considerado para o plote \n')


path_dark = ask_file_path("dark-CELIV")

while not is_valid_file(path_dark):
    message_invalid_path()
    path_dark = ask_file_path("dark-CELIV")

dark_CELIV = pd.read_table(path_dark, sep='\t', header=None)

current_dark_celiv_ramp_time = separate_even_columns(dark_CELIV).abs()

path_photo = ask_file_path("photo_celiv")

while not is_valid_file(path_photo):
    message_invalid_path()
    path_photo = ask_file_path("photo-celiv")

current_photo_celiv_ramp_time = (separate_even_columns(pd.read_table(path_photo, sep='\t', header=None))).abs()

time_photo_celiv_ramp_time = separate_odd_columns(pd.read_table(path_photo, sep='\t', header=None))

even_columns_subtraction = pd.DataFrame(current_photo_celiv_ramp_time - current_dark_celiv_ramp_time)

data_ramp_time = pd.concat([time_photo_celiv_ramp_time, even_columns_subtraction],
                           axis=1).sort_index(1, 1)

data_ramp_time.to_csv(ask_file_name(), sep='\t')

data_ramp_time_transposed_in_arrays = data_ramp_time.transpose().to_np()


integrated_val = integrate.simps(
    data_ramp_time_transposed_in_arrays[3],
    data_ramp_time_transposed_in_arrays[2],
    axis=-1, even='avg')

print(integrated_val)
