import requests
import json
from datetime import datetime, timedelta
import time
headers =   {
    'accept': '*/*',
    'accept-language': 'fr-FR,fr;q=0.9,en;q=0.8',
    'authorization': 'Bearer undefined',
    'referer': 'https://web.archive.org/web/20190101/https://meteofrance.com/',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'x-pywb-requested-with': 'XMLHttpRequest',
}
base = "https://web.archive.org/web/"
urls = [
     "https://rpcache-aa.meteofrance.com/internet2018client/2.0/multiforecast?bbox=&coords=41.925112%2C8.735601_48.428983%2C0.091053_49.89149%2C2.297577_44.925048%2C2.439111_47.79735%2C3.565884_47.640776%2C6.849168_43.48056%2C-1.55_44.837098%2C-0.580433_45.616508%2C6.768147_47.083316%2C2.394478_48.389778%2C-4.487512_46.793127%2C4.846777_48.110332%2C5.137971_49.63838%2C-1.616008_44.558371%2C6.077558_46.158668%2C-1.151253_50.631573%2C3.057161_45.833929%2C1.260532_45.758097%2C4.8407_43.296199%2C5.375945_49.119505%2C6.176565_44.557726%2C4.750725_43.610355%2C3.875467_47.2165%2C-1.554608_43.701513%2C7.26712_48.859333%2C2.340591_42.697131%2C2.8942_49.264376%2C4.027926_48.113628%2C-1.681487_49.442428%2C1.102139_48.583085%2C7.746694_43.232608%2C0.073956_43.604098%2C1.441079_47.391812%2C0.687256_46.126251%2C3.424781&begin_time=&end_time=&time=&instants=morning%2Cafternoon%2Cevening%2Cnight",
    'https://rpcache-aa.meteofrance.com/internet2018client/2.0/multiforecast?bbox=&liste_id=200040%2C610010%2C800210%2C150140%2C890240%2C900100%2C641220%2C330630%2C730540%2C180330%2C290190%2C710760%2C521210%2C501290%2C050610%2C173000%2C593500%2C870850%2C691230%2C130550%2C574630%2C261980%2C341720%2C441090%2C060880%2C751010%2C661360%2C514540%2C352380%2C765400%2C674820%2C654400%2C315550%2C372610%2C033100&begin_time=&end_time=&time=&instants=morning%2Cafternoon%2Cevening%2Cnight',
   ]

url = "https://web.archive.org/web/20200902/https://rpcache-aa.meteofrance.com/internet2018client/2.0/multiforecast?bbox=&liste_id=200040%2C610010%2C800210%2C150140%2C890240%2C900100%2C641220%2C330630%2C730540%2C180330%2C290190%2C710760%2C521210%2C501290%2C050610%2C173000%2C593500%2C870850%2C691230%2C130550%2C574630%2C261980%2C341720%2C441090%2C060880%2C751010%2C661360%2C514540%2C352380%2C765400%2C674820%2C654400%2C315550%2C372610%2C033100&begin_time=&end_time=&time=&instants=morning%2Cafternoon%2Cevening%2Cnight"
setDate = set()
# Début et fin de la période
start_date = datetime(2020, 8, 30)
end_date = datetime.now()

# Création d'une liste pour stocker les dates
dates_list = set()
weather_data = dict()
# Itération sur la période
with open('resultMeteo.csv', 'a+',encoding="utf-8") as f:
    f.write('j1,j2,T_min,T_max,daily_weather_description\n')
    for url in urls:
        current_date = start_date
        while current_date <= end_date:
            current_date += timedelta(days=1)
            if str(current_date.strftime('%Y-%m-%d')) not in setDate:
                dates_list.add(current_date.strftime('%Y-%m-%d'))
                complete_url = base + str(current_date.strftime('%Y%m%d')) + '/' + url
                try:
                    response = requests.get(complete_url, headers=headers)
                except requests.exceptions.RequestException as e:
                    print(f"Une erreur s'est produite : {e}")
                    time.sleep(10)  # Pause de 10 secondes
                    current_date -= timedelta(days=1)
                    continue
                # Charger la chaîne JSON dans un dictionnaire Python
                if response.status_code != 200:
                    print('Error: ', response.status_code)
                    continue
                data_dict = json.loads(response.text)

                # Parcourir chaque feature dans la liste des features
                for feature in data_dict['features']:
                    if feature['properties']['name'] == 'Montpellier':
                        # Extraire et afficher les informations de Montpellier
                        montpellier_info = feature
                        break
                date_reel = montpellier_info["update_time"][:10]
                # Afficher les informations de Montpellier, si trouvées
                for data in montpellier_info['properties']['daily_forecast']:
                    date_prev =  data['time'][:10]
                    if datetime.strptime(date_reel, '%Y-%m-%d') <= datetime.strptime(date_prev, '%Y-%m-%d') - timedelta(days=7):
                        setDate.add(date_reel)
                        weather_data[date_prev] = {
                            'j1' : date_reel,
                            'T_min': data['T_min'],
                            'T_max': data['T_max'],
                            'daily_weather_description': data['daily_weather_description']
                        }
                        print(date_reel,date_prev, data['T_min'], data['T_max'], data['daily_weather_description'])
                        f.write(f"{date_reel},{date_prev},{data['T_min']},{data['T_max']},{data['daily_weather_description']}\n")
                        f.flush()
        

# # Compare les deux listes
print(dates_list - setDate)