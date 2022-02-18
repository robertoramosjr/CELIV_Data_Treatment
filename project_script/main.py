import sys
import os.path
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate

teste 123

def separate_even_columns(data_frame):
    return data_frame.iloc[:, [i for i in range(len(data_frame.columns)) if i % 2 == 1]]


def separate_odd_columns(data_frame):
    return data_frame.iloc[:, [i for i in range(len(data_frame.columns)) if i % 2 == 0]]


# def integrate_data_frame(data_frame):
#     return data_frame\
#         .apply(lambda g: integrate.trapz(g.separate_even_columns(data_frame), x=g.separate_odd_columns(data_frame)))


def is_valid_file(file_path):
    return True if file_path != "" and os.path.exists(file_path) else False


def ask_file_path(measurement_name):
    return input(f"Insira o caminho do arquivo do {measurement_name} ramptime \n")


def message_invalid_path():
    return print("Arquivo inválido ou inexistente \n")


def ask_file_name():
    return input("Insira o nome do arquivo para salvar \n")


def plot_the_data(data_frame, x_axys, y_axyx):
    return data_frame.plot(x=f'{x_axys}', y=f'{y_axyx}', kind='line')


def ask_x_axys():
    return input('Insira o cabeçalho do eixo x a ser considerado para o plote \n')


def ask_y_axys():
    return input('Insira o cabeçalho do eixo y a ser considerado para o plote \n')


path_dark = ask_file_path("dark-CELIV")

while not is_valid_file(path_dark):
    message_invalid_path()
    path_dark = ask_file_path("dark-CELIV")

dark_CELIV = pd.read_table(path_dark, sep='\t')

current_dark_celiv_ramp_time = separate_even_columns(dark_CELIV).abs()

x = ask_x_axys()

y = ask_y_axys()

# plot_the_data(dark_CELIV, x, y)
# plt.show()

path_photo = ask_file_path("photo_celiv")

while not is_valid_file(path_photo):
    message_invalid_path()
    path_photo = ask_file_path("photo-celiv")

current_photo_celiv_ramp_time = (separate_even_columns(pd.read_table(path_photo, sep='\t', header=None))).abs()

time_photo_celiv_ramp_time = separate_odd_columns(pd.read_table(path_photo, sep='\t', header=None))

even_columns_subtraction = pd.DataFrame(current_photo_celiv_ramp_time - current_dark_celiv_ramp_time)

data_ramp_time = pd.concat([time_photo_celiv_ramp_time, even_columns_subtraction], axis=1).sort_index(1, 1)

# data_ramp_time.to_csv(ask_file_name(), sep='\t')

# pd.DataFrame(integrate_data_frame(data_ramp_time)).to_csv(ask_file_name(), sep='\t')
