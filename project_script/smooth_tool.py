import pandas as pd
import ask
import messages as msgs
import datatreatment as dt
import numpy as np
import matplotlib.pyplot as plt

results_path = ask.file_path("para suavizar")

meas_number = 2 * (int(input('Qual o número de medidas para suavizar? \n')))

while not dt.is_valid_file(results_path):
    msgs.message_invalid_path()
    results_path = ask.file_path("para suavizar")

results = pd.read_table(results_path, sep='\t', decimal=',', header=None).iloc[1:, :]
to_smooth = dt.separate_odd_columns(results).transpose().to_numpy()
to_reunite = dt.separate_even_columns(results)
to_plot = to_reunite.transpose().to_numpy()

smoothed = np.array(dt.smooth_current_noise(to_smooth))

smoothed_dataframe = pd.DataFrame(smoothed).transpose().set_axis(list(range(1, meas_number, 2)), axis=1)

for k, v in enumerate(smoothed):
    plt.plot(to_plot[k], smoothed[k])
plt.xlabel('Time (\u03BC s)')
plt.ylabel('\u0394 j (mA/cm\u00B2)')

plt.show()

smoothed_data = pd.concat([to_reunite, smoothed_dataframe], axis=1).sort_index(axis=1, ascending=True)

smoothed_data.to_csv(
        ask.file_name('resultados suavizados').replace('\\', '/'),
        sep='\t',
        index=False,
        decimal=',',
        header=False
    )
