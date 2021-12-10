# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from datetime import datetime

import requests
import json

apiKey = 'ARU5uGFL5Uq1OXr2lHP0QyujAStUvfIU'
apiSecret = 'KOZpmXWD7OOMwmgx'
resposta = {
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

meses = {'january': '01',
        'february': '02',
        'march': '03',
        'april': '04',
        'may': '05',
        'june': '06',
        'july': '07',
        'august': '08',
        'september': '09',
        'october': '10',
        'november': '11',
        'december': '12'
}

dias = {'first': '01',
        'second': '02',
        'third': '03',
        'forth': '04',
        'fifth': '05',
        'sixth': '06',
        'seventh': '07',
        'eighth': '08',
        'ninth': '09',
        'tenth': '10', 
        'eleventh': '11',
        'twelfth': '12',
        'thirteenth': '13',
        'fourteenth': '14',
        'fifteenth': '15',
        'sixteenth': '16',
        'seventeenth': '17',
        'eighteenth': '18',
        'nineteenth': '19',
        'twentieth': '20',
        'twenty-first': '21',
        'twenty-second': '22',
        'twenty-third': '23',
        'twenty-fourth': '24',
        'twenty-fifth': '25',
        'twenty-sixth': '26',
        'twenty-seventh': '27',
        'twenty-eigth': '28',
        'twenty-ninth': '29',
        'thirtieth': '30',
        'thirty-first': '31'
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

        mes = meses[tracker.get_slot('depart_date.month_name')]
        dia = dias[tracker.get_slot('depart_date.day_number').replace(' ', '-')]

        hoje = datetime.today()

        formats = ["%B %d", "%d %B", "%b %d", "%m/%d", "%m %d"]
        dates = mes + ' ' + dia

        date = dates.lower().replace("rd", "").replace("nd", "").replace("st", "")

        for format in formats:
            #print(datetime.strptime(date, format).strftime("%m/%d/%Y"))
            try:
                dataVoo = datetime.strptime(date, format).strftime("2021-%m-%d")
            except ValueError:
                pass
        
        sep = dataVoo.split('-')
        dataVoo = datetime(int(sep[0]), int(sep[1]), int(sep[2]))

        if dataVoo < hoje:
            dataVoo = datetime(2022, int(sep[1]), int(sep[2]))
        print(dataVoo.strftime('%Y-%m-%d'))
        params = (
            ('originLocationCode', str(fromCity)),
            ('destinationLocationCode', str(toCity)),
            ('departureDate', str(dataVoo.strftime('%Y-%m-%d'))),
            ('adults', 1),
        )

        response2 = requests.get('https://test.api.amadeus.com/v2/shopping/flight-offers', headers=headers, params=params)

        dicti2 = json.loads(response2.text)

        if dicti2['meta']['count'] != 0:
            print(dicti2['data'][0])
            dispatcher.utter_message(text='You can go for '+str(dicti2['data'][0]['price']['total']))
        else:
            dispatcher.utter_message(text='Sorry, we couldnt find flights from ' + str(tracker.get_slot('fromloc.city_name')) + ' to ' + str(tracker.get_slot('toloc.city_name')) + ' on ' + dataVoo.strftime("%Y-%m-%d"))
        return []


class ActionQA(Action):

    def name(self) -> Text:
        return "action_qa"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent = tracker.get_intent_of_latest_message()
        print(intent)
        if intent == "meal":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')
            airline = tracker.get_slot('airline_name')

            message=''

            if airline != None:
                meals =''
                # we have the options {meal} for ...
                newA = airline.replace(' ', '_')
                if newA in resposta[intent].keys():
                    meals_vec = resposta[intent][newA]
                    if len(meals_vec) == 1: 
                        message = f"We have the option of {meals_vec[0]} for the airline {airline.upper()}"
                    else:
                        for meal in meals_vec[:-1]:
                            meals = meals + f" {meal},"
                        meals = meals[:-1] + f" and {meals_vec[-1]}"
                        message = f"We have the options of {meals} for the airline {airline.upper()}"
                else:
                    message = f"Sorry we dont have informations about the meals for the airline {airline.upper()}"
            else:
                meals =''
                # we have the options {meal} for ...
                key = f"{fromloc}+{toloc}".replace(' ', '_')

                if key in resposta[intent].keys():
                    meals_vec = resposta[intent][key]
                    if len(meals_vec) == 1: 
                        message = f"We have the option of {meals_vec[0]} for the flight between {fromloc.upper()} and {toloc.upper()}"
                    else:
                        for meal in meals_vec[:-1]:
                            meals = meals + f" {meal},"
                        meals = meals[:-1] + f" and {meals_vec[-1]}"
                        message = f"We have the options of {meals} for the flight between {fromloc.upper()} and {toloc.upper()}"
                else:
                    message = f"Sorry we dont have informations about the meals for the flight between {fromloc.upper()} and {toloc.upper()}"

            dispatcher.utter_message(text=message)

        elif intent == "restriction":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')

            message = ''
            key = f"{fromloc}+{toloc}".replace(' ', '_')

            if key in resposta[intent].keys():
                items = ''
                vec = resposta[intent][key]
                if len(vec) == 1: 
                    message = f"The costumer have the obrigation to have {vec[0]} for the flight between {fromloc.upper()} and {toloc.upper()}"
                else:
                    for item in vec[:-1]:
                        items = items + f" {item},"
                    items = items[:-1] + f" and {vec[-1]}"
                    message = f"The costumer have the obrigation to have {items} for the flight between {fromloc.upper()} and {toloc.upper()}"
            else:
                message = f"Sorry we dont have informations about the restrictions for the flight between {fromloc.upper()} and {toloc.upper()}"

            dispatcher.utter_message(text=message)



        elif intent == "capacity":
            airline = tracker.get_slot('airline_name')
            aircraft_code = tracker.get_slot('aircraft_code')

            message = ''

            if airline != None:
                key = airline.replace(' ', '_')

                if key in resposta[intent].keys():
                    items = ''
                    vec = resposta[intent][key]
                    if len(vec) == 1: 
                        message = f"The airline {airline.upper()} has airplanes with the capacity of {vec[0]}"
                    else:
                        for item in vec[:-1]:
                            items = items + f" {item},"
                        items = items[:-1] + f" and {vec[-1]}"
                        message = f"The airline {airline.upper()} has airplanes with the capacity of {items}"
                else:
                    message = f"Sorry we dont have informations about capacity for the airline {airline.upper()}"

            else:
                key = aircraft_code.replace(' ', '_')

                if key in resposta[intent].keys():
                    items = ''
                    vec = resposta[intent][key]
                    if len(vec) == 1: 
                        message = f"The aircraft {aircraft_code} has the capacity of {vec[0]}"
                    else:
                        for item in vec[:-1]:
                            items = items + f" {item},"
                        items = items[:-1] + f" and {vec[-1]}"
                        message = f"The aircraft {aircraft_code} has the capacity of {items}"
                else:
                    message = f"Sorry we dont have informations about capacity for the aircraft {airline.upper()}"

            dispatcher.utter_message(text=message)


        elif intent == "quantity":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')

            message = ''
            key = f"{fromloc}+{toloc}".replace(' ', '_')

            if key in resposta[intent].keys():
                vec = resposta[intent][key]
                message = f"The fight between {fromloc.upper()} and {toloc.upper()} has {vec[0]} flights that stop at least once and {vec[1]} direct flights"
            else:
                message = f"Sorry we dont have informations about the quantify of flights for the flight between {fromloc.upper()} and {toloc.upper()}"

            dispatcher.utter_message(text=message)


        elif intent == "ground_fare":
            city = tracker.get_slot('city_name')
            airportName = tracker.get_slot('fromloc.airport_name')
            airportName = tracker.get_slot('airport_name')
            message = ""

            if city != None:
                key = city.replace(' ', '_')
                if key in resposta[intent].keys():
                    vec = resposta[intent][key]
                    message = f"The ground fares are {vec[0]}$ for a Limusine and {vec[1]} for a normal car at {city.upper()}"
                else:
                    message = f"Sorry we dont have informations about the ground fares at {city.upper()}"

            else:
                print(airportName)
                key = airportName.replace(' ', '_')
                if key in resposta[intent].keys():
                    vec = resposta[intent][key]
                    message = f"The ground fares are {vec[0]}$ for a Limusine and {vec[1]}$ for a normal car at {airportName.upper()}"
                else:
                    message = f"Sorry we dont have informations about the ground fares at {airportName.upper()}"

            dispatcher.utter_message(text=message)

        elif intent == "distance":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')
            message = ''
            key = f"{fromloc}+{toloc}".replace(' ', '_')

            if key in resposta[intent].keys():
                vec = resposta[intent][key]
                message = f"The fight between {fromloc.upper()} and {toloc.upper()} has a distance of {vec[0]} miles"
            else:
                message = f"Sorry we dont have informations about the distance for the flights between {fromloc.upper()} and {toloc.upper()}"

            dispatcher.utter_message(text=message)


        elif intent == "airline":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')

            message = ''
            key = f"{fromloc}+{toloc}".replace(' ', '_')

            if key in resposta[intent].keys():
                items = ''
                vec = resposta[intent][key]
                if len(vec) == 1: 
                    message = f"We have the airline {vec[0]} for the flight between {fromloc.upper()} and {toloc.upper()}"
                else:
                    for item in vec[:-1]:
                        items = items + f" {item},"
                    items = items[:-1] + f" and {vec[-1]}"
                    message = f"We have the airlines {items} for the flights between {fromloc.upper()} and {toloc.upper()}"
            else:
                message = f"Sorry we dont have informations about the airlines for the flights between {fromloc.upper()} and {toloc.upper()}"

            dispatcher.utter_message(text=message)



        elif intent == "airport":
            city = tracker.get_slot('city_name')

            message = ''
            key = city.replace(' ', '_')

            if key in resposta[intent].keys():
                items = ''
                vec = resposta[intent][key]
                if len(vec) == 1: 
                    message = f"We have the airport {vec[0]} at {city.upper()}"
                else:
                    for item in vec[:-1]:
                        items = items + f" {item},"
                    items = items[:-1] + f" and {vec[-1]}"
                    message = f"We have the airport {items} at {city.upper()}"
            else:
                message = f"Sorry we dont have informations about the airports at {city.upper()}"

            dispatcher.utter_message(text=message)


        elif intent == "ground_service":
            city = tracker.get_slot('city_name')
            fromloc = tracker.get_slot('fromloc.city_name')

            message = ""

            if city != None:
                key = city.replace(' ', '_')
                if key in resposta[intent].keys():
                    items = ''
                    vec = resposta[intent][key]
                    if len(vec) == 1: 
                        message = f"We have the ground service {vec[0]} at {city.upper()}"
                    else:
                        for item in vec[:-1]:
                            items = items + f" {item},"
                        items = items[:-1] + f" and {vec[-1]}"
                        message = f"We have the ground services {items} at {city.upper()}"
                else:
                    message = f"Sorry we dont have informations about the ground services at {city.upper()}"

            else:
                key = fromloc.replace(' ', '_')
                if key in resposta[intent].keys():
                    items = ''
                    vec = resposta[intent][key]
                    if len(vec) == 1: 
                        message = f"We have the ground service {vec[0]} at {fromloc.upper()}"
                    else:
                        for item in vec[:-1]:
                            items = items + f" {item},"
                        items = items[:-1] + f" and {vec[-1]}"
                        message = f"We have the ground service {vec[0]} at {fromloc.upper()}"
                else:
                    message = f"Sorry we dont have informations about the ground services at {fromloc.upper()}"

            dispatcher.utter_message(text=message)


        elif intent == "aircraft":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')

            message = ''
            key = f"{fromloc}+{toloc}".replace(' ', '_')

            if key in resposta[intent].keys():
                items = ''
                vec = resposta[intent][key]
                if len(vec) == 1: 
                    message = f"We have the aircraft {vec[0]} for the flight between {fromloc.upper()} and {toloc.upper()}"
                else:
                    for item in vec[:-1]:
                        items = items + f" {item},"
                    items = items[:-1] + f" and {vec[-1]}"
                    message = f"We have the aircraft {items} for the flights between {fromloc.upper()} and {toloc.upper()}"
            else:
                message = f"Sorry we dont have informations about the aircrafts for the flights between {fromloc.upper()} and {toloc.upper()}"

            dispatcher.utter_message(text=message)

        else:
            dispatcher.utter_message(text='Error intent not listed')
