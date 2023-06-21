import urllib.request
import urllib.parse
import urllib.error
import json

serviceurl = 'https://nominatim.openstreetmap.org/reverse.php?'

while True:
    address = input('Enter location: ')

    if len(address) < 1:
        break
    lat = input('Enter latitude: ')
    lon = input('Enter longitude: ')
    if len(lat) < 1 or len(lon) < 1:
        break

    url = serviceurl + urllib.parse.urlencode(
        {'lat': lat, 'lon': lon, 'format': 'jsonv2'})

    # print('Retrieving', url)
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    # print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'error' in js:
        print('==== Failure To Retrieve ====')
        # print(data)
        continue

    # print(json.dumps(js, indent=4))
    print(js['display_name'])
    print(js['address']['house_number'])
    print(js['address']['road'])
    print(js['address']['city'])
    print(js['address']['postcode'])
    print(js['address']['country'])
    print(js['address']['country_code'])
    break
