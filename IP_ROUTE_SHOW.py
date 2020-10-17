import webbrowser
from subprocess import Popen, PIPE
import gmplot
from ip2geotools.databases.noncommercial import DbIpCity
from requests import get

hostname = "www.gov.uk"
p = Popen("cmd /c tracert " + hostname, shell=True, stdout=PIPE, encoding='utf-8')

destination_IP = 0
IP_list = []
i = 0
for line in p.stdout:
    x = line.rstrip('\n')
    y = x.split()
    if len(y) > 0:
        y[-1] = y[-1].replace("[", "")
        y[-1] = y[-1].replace("]", "")
        if y[-1][0].isalpha() == False:
            if i == 0:
                destination_IP = y[-1]
                i += 1
                print(f'Destination IP: {y[-1]}')
            else:
                IP_list.append(y[-1])
                print(f'HOP {i}: {y[-1]}')
                i += 1

if IP_list[-1] == destination_IP:
    print(f"SUCCESS IN {i - 1} HOPS")
else:
    print("PACKETS DIDN'T REACH DESTINATION")

apikey = ''  # (your API key here)
gmap = gmplot.GoogleMapPlotter(45, 0, 3, apikey=apikey)

latis = []
longs = []

i = 1

last_resp_lat = 0
last_resp_long = 0

for IP in IP_list:
    if IP.find("192") == -1:
        response = DbIpCity.get(IP, api_key='free')
    else:
        ip = get('https://api.ipify.org').text
        response = DbIpCity.get(ip, api_key='free')

    if response.latitude != last_resp_lat and response.longitude != last_resp_long:
        last_resp_lat = response.latitude
        last_resp_long = response.longitude
        gmap.marker(response.latitude, response.longitude, color='cornflowerblue', info_window=f"{IP}", label=f"{i}")
        i += 1
    latis.append(response.latitude)
    longs.append(response.longitude)

gmap.plot(lats = latis, lngs = longs, edge_width=7, color='red')
gmap.draw('map.html')

webbrowser.open('map.html')