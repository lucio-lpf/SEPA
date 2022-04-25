import requests
import csv
import json

# SET UP weather API URL
url = "http://api.worldweatheronline.com/premium/v1/weather.ashx?"
url += "key=0ec597ffa0494d6a80d185742211008"


def get_all_json_keys(keys_array, json):
    for key in json.keys():
        if not isinstance(json[key], str):
            _ = get_all_json_keys(keys_array, json[key][0])
        else:
            keys_array.append(key)
    return keys_array


def get_all_json_values(values_array, json):
    for key in json.keys():
        if not isinstance(json[key], str):
            _ = get_all_json_values(values_array, json[key][0])
        else:
            values_array.append(json[key])
    return values_array


def url_constructor(system):
    request_url = url
    request_url += "&q=" + system['lat_long']
    request_url += "&format=json"
    request_url += "&num_of_days=5"
    request_url += "&mca=no"
    request_url += "&includelocation=yes"
    request_url += "&tp=24"
    return request_url


system_list = []

with open("favorite_systems.csv", "r") as systems:
    reader = csv.reader(systems, delimiter=",")
    next(reader)
    for line in reader:
        system_dict = {}
        system_dict['id'] = line[0]
        system_dict['lat_long'] = line[14] + "," + line[15]
        system_list.append(system_dict)

for system in system_list:

    weather_list = []
    print(system['lat_long'])
    request_url = url_constructor(system)
    response = requests.get(request_url)
    if response.status_code != 200:
        print("Excedeu numedo de request")
        print(response.content)
        exit()
    content = response.content
    content = content.decode()
    content = json.loads(content)
    content = content['data']['weather']
    file_name = "./forecasting/system_" + system['id'] + ".csv"
    with open(file_name, 'w') as test_daily:

        predicton = content[0]['hourly']
        header = ','.join(get_all_json_keys([], content[0]))
        header += ',' + ','.join(get_all_json_keys([], predicton[0]))
        print(header, file=test_daily)

        for weather in content:
            predicton = weather.pop('hourly')
            row = ','.join(get_all_json_values([], weather))
            row += ',' + ','.join(get_all_json_values([], predicton[0]))
            print(row, file=test_daily)
