# from datetime import datetime

# dias = {'first': '01',
#         'second': '02',
#         'third': '03',
#         'forth': '04',
#         'fifth': '05',
#         'sixth': '06',
#         'seventh': '07',
#         'eighth': '08',
#         'nineth': '09',
#         'tenth': '10', 
#         'eleventh': '11',
#         'twelfth': '12',
#         'thirteenth': '13',
#         'fourteenth': '14',
#         'fifteenth': '15',
#         'sixteenth': '16',
#         'seventeenth': '17',
#         'eighteenth': '18',
#         'nineteenth': '19',
#         'twentieth': '20',
#         'twenty-first': '21',
#         'twenty-second': '22',
#         'twenty-third': '23',
#         'twenty-fourth': '24',
#         'twenty-fifth': '25',
#         'twenty-sixth': '26',
#         'twenty-seventh': '27',
#         'twenty-eigth': '28',
#         'twenty-ninth': '29',
#         'thirtieth': '30',
#         'thirty-first': '31'
# }

# formats = ["%B %d", "%d %B", "%b %d", "%m/%d", "%m %d"]
# dates = "march twenty-first"
# dates = dates.split(" ")
# for date in range(len(dates)):
#     try: 
#         dates[date] = dias[dates[date]]
#     except:
#         pass

# dates = " ".join(dates)
# print(dates)

# date = dates.lower().replace("rd", "").replace("nd", "").replace("st", "")
# print(datetime.today())
# for format in formats:
#     #print(datetime.strptime(date, format).strftime("%m/%d/%Y"))
#     try:
#         print(datetime.strptime(date, format).strftime("%m-%d"))
#     except ValueError:
#         pass

# from datetime import date
# from datetime import datetime

# dt = datetime(2021, 10, 12)

# print(dt)

apiKey = 'ARU5uGFL5Uq1OXr2lHP0QyujAStUvfIU'
apiSecret = 'KOZpmXWD7OOMwmgx'

import requests
import json
import pprint

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
    'grant_type': 'client_credentials',
    'client_id': apiKey,
    'client_secret': apiSecret
}

response = requests.post('https://test.api.amadeus.com/v1/security/oauth2/token', headers=headers, data=data)
dicti = json.loads(response.text)

headers = {
    'Authorization': 'Bearer ' + dicti['access_token'],
}

params = (
    ('subType', 'CITY'),
    ('keyword', 'chicago'),
)
response2 = requests.get('https://test.api.amadeus.com/v1/reference-data/locations', headers=headers, params=params)

fromCity = json.loads(response2.text)['data'][0]['iataCode']

params = (
    ('subType', 'CITY'),
    ('keyword', 'new york'),
)

response2 = requests.get('https://test.api.amadeus.com/v1/reference-data/locations', headers=headers, params=params)

toCity = json.loads(response2.text)['data'][0]['iataCode']

params = (
    ('originLocationCode', str(fromCity)),
    ('destinationLocationCode', str(toCity)),
    ('departureDate', '2021-12-15'),
    ('adults', 1),
)

response2 = requests.get('https://test.api.amadeus.com/v2/shopping/flight-offers', headers=headers, params=params)

dicti2 = json.loads(response2.text)

pprint.pprint(dicti2['data'][0])

params = (
    ('airlineCodes', 'BA'),
)

print(params)
r3 = requests.get('https://test.api.amadeus.com/v1/reference-data/airlines', headers=headers, params=params)
d3 = json.loads(r3.text)
print(d3)
