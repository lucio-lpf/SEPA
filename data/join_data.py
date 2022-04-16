import os
import sys
import pandas as pd
import numpy as np
from time_converter import date_weather_format, day_of_year


if len(sys.argv) < 2:
    print("Please, inform the data path. EX: san_francisco")
    exit()
# THE PORPOUS OF THIS SCRIPT IS TO JOIN THE INFORMATION ON THE DAILY OUTPUT AND
# WEATHER OF EACH SOLAR PANEL AND ITS LOCATION
location_dir = sys.argv[1]


if not os.path.exists(location_dir+'/join'):
    os.mkdir(location_dir+'/join')

join_dir = location_dir + '/join'
daily_outputs_dir = location_dir + '/daily_outputs'
weather_dir = location_dir + '/weathers'


# THE COLUMNS THAT WILL BE USED FOR MACHINE LEARNING
columns = ['date', 'totalSnow_cm', 'mintempC', 'avgtempC',
           'uvIndex', 'WindChillC', 'cloudcover', 'winddirDegree',
           'WindGustKmph', 'HeatIndexC', 'precipMM', 'FeelsLikeC',
           'visibility', 'humidity', 'pressure', 'DewPointC', 'windspeedKmph',
           'maxtempC']

columns_join = ['Efficiency', 'System Size',
                'Number Of Panels', 'Panel Power', 'Number Of Inverters',
                'Inverter Power'] + columns


def file_header(daily_file, weather_file, favorites_file, out_file):
    all_columns = np.append(daily_file.columns, weather_file.columns)
    all_columns = np.append(all_columns, favorites_file.columns)
    all_columns = all_columns.tolist()
    print(",".join(all_columns), file=out_file)


print_header = True
# FOR EACH SYSTEM RECORDS FILE
for filename in os.listdir(daily_outputs_dir):

    with open(location_dir+'/join/unfiltered_data.csv', 'a') as out_file:
        sys_id = filename.split("_")[2]
        print("Combining system:", sys_id)
        weather_path = weather_dir + '/system_' + sys_id + '.csv'
        favorites_path = location_dir + '/favorite_systems.csv'
        favorites_file = pd.read_csv(favorites_path)
        try:
            weather_file = pd.read_csv(weather_path)
            weather_file = weather_file[columns]
        except Exception:
            # IF THERE IS NO FILE WITH WEATHER INFORMATION CONTINUE TO NEXT
            # PV SYSTEM
            continue

        daily_file = pd.read_csv(daily_outputs_dir + "/" + filename)
        daily_file = daily_file.drop_duplicates(subset="Date")

        # PRINT ALL THE INDEX IN THE JOIN FILE
        if print_header is True:
            file_header(daily_file, weather_file, favorites_file, out_file)
            print_header = False

        # FINDS THE PV SYSTEM CHARACTERISTICS
        selected_system = None
        for row in favorites_file.values:
            if int(row[0]) == int(filename.split("_")[2]):
                selected_system = row

        if selected_system is None:
            continue

        # MATCH THE DATE FROM EACH FILE ROWS
        count_rows_weather = 0
        for row in daily_file.values:
            if row[2] < 0.1:
                continue
            # import pdb; pdb.set_trace()
            daily_date = date_weather_format(str(row[0]))
            weather_date = weather_file['date'].values[count_rows_weather]
            # CHECK IF DATES MATCH (SOMETIMES THERE ARE PV RECORDS MISSING)
            while daily_date != weather_date:
                print(daily_date, weather_date)
                count_rows_weather += 1
                weather_date = weather_file['date'].values[count_rows_weather]

            # CONVERTS DATE INTO THE DAY OF THE YEAR TO DIVIDE INTO SEASONS
            day = day_of_year(weather_date)
            weather_file['date'].values[count_rows_weather] = day

            # USES NUMPY ARRAY TO COMBINE ALL DATA FEATURES
            all_values = np.append(row,
                                   weather_file.values[count_rows_weather])
            all_values = np.append(all_values, selected_system)
            all_values = all_values.tolist()

            print(",".join(str(e) for e in all_values), file=out_file)

# FILTERS CORRUPED DATA AND DROP UNECESSARY COLUMNS
join_file = pd.read_csv(location_dir+'/join/unfiltered_data.csv')
join_file.drop(join_file[join_file['Condition'] == 'Not Sure'].index,
               inplace=True)
join_file = join_file[columns_join]

join_file.to_csv(location_dir+'/join/join_data.csv', index=False,
                 float_format='%.3f')
# todo separa em varios dataset
