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
    {'airline':'aiai', 'fromloctoloc':'aiai2'
    },
    'capacity':
    {'airline':'aiai', 'fromloctoloc':'aiai2'
    },
    'quantity':
    {'airline':'aiai', 'fromloctoloc':'aiai2'
    },
    'ground_fare':
    {'airline':'aiai', 'fromloctoloc':'aiai2'
    },
    'distance':
    {'airline':'aiai', 'fromloctoloc':'aiai2'
    },
    'airline':
    {'airline':'aiai', 'fromloctoloc':'aiai2'
    },
    'airport':
    {'airline':'aiai', 'fromloctoloc':'aiai2'
    },
    'ground_service':
    {'airline':'aiai', 'fromloctoloc':'aiai2'
    },
    'aircraft':
    {'airline':'aiai', 'fromloctoloc':'aiai2'
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
