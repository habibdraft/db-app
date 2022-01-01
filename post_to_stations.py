import requests
import json
from bart_api import BartApi

def xml_to_dict(elem):
    if elem.text == None and len(elem.attrib):
        return elem.tag, elem.attrib
    return elem.tag, dict(map(xml_to_dict, elem)) or elem.text

bart = BartApi()
stations = bart.get_stations()

url = 'http://127.0.0.1:5000/stations/'
headers = {"Content-Type": "application/json; charset=utf-8"}

for station in stations:
    d = xml_to_dict(station)
    response = requests.post(url, headers=headers, json=d[1])
    print("Status Code", response.status_code)
    print("JSON Response ", response.json())
