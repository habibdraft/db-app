import requests
import json
from bart_api import BartApi

bart = BartApi()
stations = bart.get_stations()

def xml_to_dict(element):
    if element.text == None and len(element.attrib):
        return element.tag, element.attrib
    return element.tag, dict(map(xml_to_dict, element)) or element.text

url = 'http://127.0.0.1:5000/stations/'
headers = {"Content-Type": "application/json; charset=utf-8"}

for station in stations:
    d = xml_to_dict(station)
    response = requests.post(url, headers=headers, json=d[1])
    print("Status Code", response.status_code)
    print("JSON Response ", response.json())
