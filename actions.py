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
            ('originLocationCode', 'REC'),
            ('destinationLocationCode', 'GRU'),
            ('departureDate', '2021-12-15'),
            ('adults', 1),
        )

        response2 = requests.get('https://test.api.amadeus.com/v2/shopping/flight-offers', headers=headers, params=params)

        dicti2 = json.loads(response2.text)

        pprint.pprint(dicti2['data'][0])
        dispatcher.utter_message(text='You can go for '+str(dicti2['data'][0]['price']['total']))
        print(dicti2['data'])

        return []
