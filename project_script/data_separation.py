import pandas as pd
import ask
import messages as msgs
import datatreatment as dt

meas_number = ask.meas_number('calculos')
results_path = ask.file_path("calculos")

while not dt.is_valid_file(results_path):
    msgs.message_invalid_path()
    results_path = ask.file_path("calculos")

results = pd.read_table(results_path, sep='\t')

results_rearranged = pd.DataFrame()
for value in range(0, meas_number):
    results_rearranged = pd.concat([results_rearranged, results.iloc[value::meas_number, :].reset_index()], axis=1)\
        .drop(labels='index', axis=1)
results_rearranged.to_csv(ask.file_name('calculos organizados').replace('\\', '/'), sep='\t', index=False)


