import os
import pandas as pd
import numpy as np
from time_converter import date_weather_format, day_of_year

# THE PORPOUS OF THIS FILE IS TO JOIN THE INFORMATION ON THE DAILY OUTPUT AND
# WEATHER OF EACH SOLAR PANEL AND ITS LOCATION

forecasting_dir = './forecasting'

# THE COLUMNS THAT WILL BE USED FOR MACHINE LEARNING
columns = ['date', 'totalSnow_cm', 'mintempC', 'avgtempC',
           'uvIndex', 'WindChillC', 'cloudcover', 'winddirDegree',
           'WindGustKmph', 'HeatIndexC', 'precipMM', 'FeelsLikeC',
           'visibility', 'humidity', 'pressure', 'DewPointC', 'windspeedKmph',
           'maxtempC']

columns_join = ['System Size', 'Number Of Panels', 'Panel Power',
                'Number Of Inverters', 'Inverter Power'] + columns


favorites_file = pd.read_csv('./favorite_systems.csv')

for filename in os.listdir(forecasting_dir):
    sys_id = filename.split("_")[1].split('.')[0]
    print(sys_id)

    selected_system = []
    for row in favorites_file.values:
        if str(row[0]) == str(sys_id):
            selected_system = row

    with open('./join_f/join_' + sys_id, 'w') as out_file:

        fc_file = pd.read_csv('./forecasting/' + filename)

        all_columns = np.append(favorites_file.columns, fc_file.columns)
        print(",".join(all_columns), file=out_file)

        for row in fc_file.values:
            row[0] = day_of_year(row[0])
            all_values = np.append(selected_system, row)
            all_values = all_values.tolist()
            print(",".join(str(e) for e in all_values), file=out_file)

    final = pd.read_csv('./join_f/join_' + sys_id)
    final = final[columns_join]
    final.to_csv('./join_f/join_' + sys_id, index=False,
                     float_format='%.3f')
