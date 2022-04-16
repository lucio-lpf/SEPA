import csv
import sys
import pandas as pd
from time_converter import day_of_year

if len(sys.argv) < 2:
    print("Please, inform the data path. EX: san_francisco")
    exit()

location_dir = sys.argv[1]

summer = open(location_dir+"/join/summer_data.csv", 'w')
fall = open(location_dir+"/join/fall_data.csv", 'w')
winter = open(location_dir+"/join/winter_data.csv", 'w')
spring = open(location_dir+"/join/spring_data.csv", 'w')

join_data = pd.read_csv(location_dir+"/join/join_data.csv")

print(','.join(join_data.columns.values), file=summer)
print(','.join(join_data.columns.values), file=fall)
print(','.join(join_data.columns.values), file=winter)
print(','.join(join_data.columns.values), file=spring)

with open(location_dir+"/join/join_data.csv", 'r') as data:
    csv_reader = csv.reader(data)
    next(csv_reader)
    for row in csv_reader:
        day = int(row[6])
        if day > 356 or day <= 80:
            print(','.join(row), file=winter)
        elif day > 80 and day <= 172:
            print(','.join(row), file=spring)
        elif day > 172 and day <= 266:
            print(','.join(row), file=summer)
        else:
            print(','.join(row), file=fall)
        #
        # if day > 335 or day <= 59:
        #     print(','.join(row), file=summer)
        # elif day > 59 and day <= 151:
        #     print(','.join(row), file=fall)
        # elif day > 151 and day <= 243:
        #     print(','.join(row), file=winter)
        # else:
        #     print(','.join(row), file=spring)

print("summer start:", day_of_year("2021-12-22"))
print("fall start:", day_of_year("2021-03-21"))
print("winter start:", day_of_year("2021-06-21"))
print("spring start:", day_of_year("2021-09-23"))
