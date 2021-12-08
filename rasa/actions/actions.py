# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests
import json

apiKey = 'ARU5uGFL5Uq1OXr2lHP0QyujAStUvfIU'
apiSecret = 'KOZpmXWD7OOMwmgx'
respostas = {
    'meal':
    {'atlanta+washington': ['fish', 'beef', 'vegetarian'], 
    'delta': ['vegan', 'fish', 'chicken'],
    'boston+denver': ['bacon', 'lobster', 'noodles'],
    'american_airlines': ['tuna sandwich', 'nuts', 'juice', 'wine', 'lasagna', 'sandwich']
    },
    'restriction':
    {'pittsburgh+atlanta':['mask','vaccination certificate','negative Covid 19 test'],
    'boston+oakland':['mask','negative Covid 19 test'],
    'atlanta+washington':['mask','vaccination certificate'],
    'boston+denver':['mask','negative Covid 19 test']
    },
    'capacity':
    {'100':['256','512'],
    '72s':['1024','2048'],
    'american_airlines':['320','640','960'],
    'united_airlines':['120','240','500','720'] 
    },
    'quantity':
    {'boston+atlanta':['15','3'], #com paradas, direto
    'san_francisco+denver':['10','5'],
    'atlanta+washington':['3','1'],
    'boston+denver':['15','0']
    },
    'ground_fare':
    {'pittsburgh':['300','40'],                 #limo, carro normal
    'tacoma':['450','35'],
    'atlanta_airport':['399','50'],
    'philadelphia_international_airport':['500','100']
    },
    'distance':
    {'los_angeles+boston':['2590'],               # in miles
    'pittsburgh+san_francisco':['2260'],
    'boston+denver':['1765'],
    'atlanta+washington':['542']
    },
    'airline':
    {'los_angeles+boston':['American airlines','United airlines','Delta'],               # in miles
    'pittsburgh+san_francisco':['Delta','United airlines'],
    'boston+denver':['American airlines'],
    'atlanta+washington':['Delta']
    },
    'airport':
    {
    'orlando':['Orlando International Airport'],
    'new_york':['New York JFK International Airport','New York La Guardia Airport','Syracuse - Hancock Intl. Airport'],
    'denver':['Denver International Airport','Rocky Mountain Metropolitan Airport','Boulder Municipal Airport'],
    'boston':['Worcester Regional Airport','Logan International Airport','Manchester-Boston Regional Airport','T. F. Green Airport']
    },
    'ground_service':
    {'denver':['Uber','taxi','bus'],
    'atlanta':['Uber','bus'],
    'baltimore':['Uber','taxi'],
    'san_diego_airport':['bus']
    },
    'aircraft':
    {'cleveland+dallas':['Turboprop Aircraft','Piston Aircraft','Jets','Mid-Size Jets'],
    'pittsburgh+baltimore':['Mid-Size Jets','Regional Jets','Narrow Body Aircraft'],
    'atlanta+boston':['Wide Body Airliners','Commuter liners'],
    'boston+san_francisco':['Airbus','Concorde','Military Aircraft','Multi-role Combat']
    },
}
class ActionAPITest(Action):

    def name(self) -> Text:
        return "action_api_test"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

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
            ('keyword', str(tracker.get_slot('fromloc.city_name'))),
        )
        response2 = requests.get('https://test.api.amadeus.com/v1/reference-data/locations', headers=headers, params=params)

        fromCity = json.loads(response2.text)['data'][0]['iataCode']

        params = (
            ('subType', 'CITY'),
            ('keyword', str(tracker.get_slot('toloc.city_name'))),
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

        dispatcher.utter_message(text='You can go for '+str(dicti2['data'][0]['price']['total']))

        return []


class ActionQA(Action):

    def name(self) -> Text:
        return "action_qa"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if tracker.get_intent_of_latest_message() == "meal":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')
            airline = tracker.get_slot('airline_name')
            if airline == None:
                dispatcher.utter_message(text=f'Vai tomar no cu porra between {fromloc} and {toloc}')
            else:
                dispatcher.utter_message(text=f'porra {airline}')
        elif tracker.get_intent_of_latest_message() == "restriction":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')
        elif tracker.get_intent_of_latest_message() == "capacity":
            airline = tracker.get_slot('airline_name')
            aircraft_code = tracker.get_slot('aircraft_code')
        elif tracker.get_intent_of_latest_message() == "quantity":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')
        elif tracker.get_intent_of_latest_message() == "ground_fare":
            city = tracker.get_slot('city_name')
            airportName = tracker.get_slot('fromloc.airport_name')
        elif tracker.get_intent_of_latest_message() == "distance":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')
        elif tracker.get_intent_of_latest_message() == "airline":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')
        elif tracker.get_intent_of_latest_message() == "airport":
            city = tracker.get_slot('city_name')
        elif tracker.get_intent_of_latest_message() == "ground_service":
            city = tracker.get_slot('city_name')
            fromloc = tracker.get_slot('fromloc.city_name')
        elif tracker.get_intent_of_latest_message() == "aircraft":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')
        else:
            dispatcher.utter_message(text='não entrei')
