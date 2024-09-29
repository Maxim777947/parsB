import requests
import pprint

def get_location_info(ip):
    return requests.get(f"http://ip-api.com/json/{ip}?lang=ru").json()

print()