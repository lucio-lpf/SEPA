import requests
import sys
import os
from time_converter import date_plus_days, current_day, date_less_days


if len(sys.argv) < 2:
    print("Please, inform the data path. EX: san_francisco")
    exit()

location_dir = sys.argv[1]

if not os.path.exists(location_dir):
    os.mkdir(location_dir)
    os.mkdir(location_dir+'/daily_outputs')

# FILE HEADERS
daily_file_header = 'Date,Energy Generated,Efficiency,Energy Exported,'
daily_file_header += 'Energy Used,Peak Power,Peak Time,Condition,'
daily_file_header += 'Min. Temperature,Max. Temperature,'
daily_file_header += 'Peak Energy Import,Off-Peak Energy Import,'
daily_file_header += 'Shoulder Energy Import,'
daily_file_header += 'High-Shoulder Energy Import,Insolation'

systems_file_header = 'System Id,System Name,System Size,Postcode,'
systems_file_header += 'Number Of Panels,Panel Power,Panel Brand,'
systems_file_header += 'Number Of Inverters,Inverter Power,Inverter Brand,'
systems_file_header += 'Orientation,Array Tilt,Shade,Install Date,'
systems_file_header += 'Latitude,Longitude,Status Interval'

# PVOUTPUT API REQUESTS CONFIG
get_system_url = "https://pvoutput.org/service/r2/getsystem.jsp"
get_favorites_url = "https://pvoutput.org/service/r2/getfavourite.jsp"
get_daily_url = "https://pvoutput.org/service/r2/getoutput.jsp"


params = {
    "sid1": "27294",
    "limit": 150,
    "insolation": 1
}

header = {
    "X-Pvoutput-Apikey": "299bcdec4112b488c5d7d20f95b71901923c53b9",
    "X-Pvoutput-SystemId": "75619"
}


# GET ALL THE SELECTED SYSTEMS
response = requests.get(get_favorites_url, headers=header)
if response.status_code != 200:
    exit()
content = response.content
content = content.decode('latin1')
with open(location_dir+"/favorite_systems.csv", 'w') as favorite_file:
    print(systems_file_header, file=favorite_file)
    print(content, end='', file=favorite_file)


# SINCE THE PV API LIMITS THE REQUESTS / HOUR I CREATED THIS REMOVES LIST TO
# KEEP THE PROGRAM OF DOING UNECESSARY REQUESTS WHEN RAN AGAIN
removes = ['52375', '29577', '55722', '70687', '8438', '41397', '13255',
           '54158', '72735', '65154', '176', '52412', '72288', '48885',
           '32239', '55434', '70830', '38742', '76398', '70775', '64779',
           '66542', '71919', '41921', '64444', '80520', '507', '33877',
           '34256', '73073', '67477', '453']

# CREATES AN ARRAY OF SYSTEMS
systems = content.split("\n")

# IGNORES THE FIRST LINE (AKA NAME OF PARAMETERS)
systems.pop(-1)


# FOR EACH SYSTEM GET ALL THE DAILY OUTPUT FROM CREATION ULTILL NOW
for solar_panel in systems:
    solar_panel = solar_panel.split(",")
    if solar_panel[0] in removes:
        continue
    print("Fetching data from system: ", solar_panel[0])
    file_name = location_dir + "/daily_outputs/solar_panel_" + solar_panel[0]
    with open(file_name, 'w') as test_daily:
        # INPUTS FILE COLUMN NAMES
        print(daily_file_header, file=test_daily)

        # FROM SYSTEM INFORMATION WE GOT THE ID AND INSTALLATION DATE
        params["sid1"] = solar_panel[0]

        # DT = DATA TO
        params["dt"] = current_day()

        status = 200
        # ARRAY TO STORE THE RESPONSE RECORDS
        daily_output = []

        # UNTIL THE APIS RETURNS 400 (DATA NOT FOUND)
        while status != 400:

            # CALLS THE API WITH THE TIME INTERVAL INSIDE THE PARAMS
            response = requests.get(get_daily_url,
                                    headers=header, params=params)

            if response.status_code == 403:
                print(response.content)
                print("Exceeded 300 requests per hour")
                print(removes)
                exit()

            status = response.status_code

            if status == 200:
                content = (response.content).decode()
                content = content.split(";")

                daily_output = daily_output + content
                params["dt"] = date_less_days(params["dt"], 150)

        # SAVES SYSTEM RECORDS IN A FILE
        for line in daily_output:
            print(line, file=test_daily)

    removes.append(solar_panel[0])
