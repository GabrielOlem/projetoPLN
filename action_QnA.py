class ActionQA(Action):

    def name(self) -> Text:
        return "action_qa"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent = tracker.get_intent_of_latest_message()
        if intent == "meal":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')
            airline = tracker.get_slot('airline_name')

            message=''

            if airline != None:
                meals =''
                # we have the options {meal} for ...
                if airline in resposta[intent].keys():
                    meals_vec = resposta[intent][airline]
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
                key = f"{fromloc}+{toloc}"

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
            key = f"{fromloc}+{toloc}"

            if key in resposta[intent].keys():
                items = ''
                vec = resposta[intent][key]
                if len(vec) == 1: 
                    message = f"The costumer have the obrigation to have {vec[0]} for the flight between {fromloc.upper()} and {toloc.upper()}"
                else:
                    for item in vec[:-1]:
                        items = items + f" {meal},"
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
                key = airline

                if key in resposta[intent].keys():
                    items = ''
                    vec = resposta[intent][key]
                    if len(vec) == 1: 
                        message = f"The airline {airline.upper()} has airplanes with the capacity of {vec[0]}"
                    else:
                        for item in vec[:-1]:
                            items = items + f" {meal},"
                        items = items[:-1] + f" and {vec[-1]}"
                        message = f"The airline {airline.upper()} has airplanes with the capacity of {items}"
                else:
                    message = f"Sorry we dont have informations about capacity for the airline {airline.upper()}"

            else:
                key = aircraft_code

                if key in resposta[intent].keys():
                    items = ''
                    vec = resposta[intent][key]
                    if len(vec) == 1: 
                        message = f"The aircraft {aircraft_code} has the capacity of {vec[0]}"
                    else:
                        for item in vec[:-1]:
                            items = items + f" {meal},"
                        items = items[:-1] + f" and {vec[-1]}"
                        message = f"The aircraft {aircraft_code} has the capacity of {items}"
                else:
                    message = f"Sorry we dont have informations about capacity for the aircraft {airline.upper()}"

            dispatcher.utter_message(text=message)


        elif intent == "quantity":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')

            message = ''
            key = f"{fromloc}+{toloc}"

            if key in resposta[intent].keys():
                vec = resposta[intent][key]
                message = f"The fight between {fromloc.upper()} and {toloc.upper()} has {vec[0]} flights that stop at least once and {vec[1]} direct flights"
            else:
                message = f"Sorry we dont have informations about the quantify of flights for the flight between {fromloc.upper()} and {toloc.upper()}"

            dispatcher.utter_message(text=message)


        elif intent == "ground_fare":
            city = tracker.get_slot('city_name')
            airportName = tracker.get_slot('fromloc.airport_name')

            message = ""

            if city != None:
                key = city
                if key in resposta[intent].keys():
                    vec = resposta[intent][key]
                    message = f"The ground fares are {vec[0]}$ for a Limusine and {vec[1]} for a normal car at {city.upper()}"
                else:
                    message = f"Sorry we dont have informations about the ground fares at {city.upper()}"

            else:
                key = airportName
                if key in resposta[intent].keys():
                    vec = resposta[intent][key]
                    message = f"The ground fares are {vec[0]}$ for a Limusine and {vec[1]} for a normal car at {airportName.upper()}"
                else:
                    message = f"Sorry we dont have informations about the ground fares at {airportName.upper()}"

            dispatcher.utter_message(text=message)

        elif intent == "distance":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')
            message = ''
            key = f"{fromloc}+{toloc}"

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
            key = f"{fromloc}+{toloc}"

            if key in resposta[intent].keys():
                items = ''
                vec = resposta[intent][key]
                if len(vec) == 1: 
                    message = f"We have the airline {vec[0]} for the flight between {fromloc.upper()} and {toloc.upper()}"
                else:
                    for item in vec[:-1]:
                        items = items + f" {meal},"
                    items = items[:-1] + f" and {vec[-1]}"
                    message = f"We have the airlines {items} for the flights between {fromloc.upper()} and {toloc.upper()}"
            else:
                message = f"Sorry we dont have informations about the airlines for the flights between {fromloc.upper()} and {toloc.upper()}"

            dispatcher.utter_message(text=message)



        elif intent == "airport":
            city = tracker.get_slot('city_name')

            message = ''
            key = city

            if key in resposta[intent].keys():
                items = ''
                vec = resposta[intent][key]
                if len(vec) == 1: 
                    message = f"We have the airport {vec[0]} at {city.upper()}"
                else:
                    for item in vec[:-1]:
                        items = items + f" {meal},"
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
                key = city
                if key in resposta[intent].keys():
                    items = ''
                    vec = resposta[intent][key]
                    if len(vec) == 1: 
                        message = f"We have the ground service {vec[0]} at {city.upper()}"
                    else:
                        for item in vec[:-1]:
                            items = items + f" {meal},"
                        items = items[:-1] + f" and {vec[-1]}"
                        message = f"We have the ground services {items} at {city.upper()}"
                else:
                    message = f"Sorry we dont have informations about the ground services at {city.upper()}"

            else:
                key = fromloc
                if key in resposta[intent].keys():
                    items = ''
                    vec = resposta[intent][key]
                    if len(vec) == 1: 
                        message = f"We have the ground service {vec[0]} at {fromloc.upper()}"
                    else:
                        for item in vec[:-1]:
                            items = items + f" {meal},"
                        items = items[:-1] + f" and {vec[-1]}"
                        message = f"We have the ground service {vec[0]} at {fromloc.upper()}"
                else:
                    message = f"Sorry we dont have informations about the ground services at {fromloc.upper()}"

            dispatcher.utter_message(text=message)


        elif intent == "aircraft":
            fromloc = tracker.get_slot('fromloc.city_name')
            toloc = tracker.get_slot('toloc.city_name')

            message = ''
            key = f"{fromloc}+{toloc}"

            if key in resposta[intent].keys():
                items = ''
                vec = resposta[intent][key]
                if len(vec) == 1: 
                    message = f"We have the aircraft {vec[0]} for the flight between {fromloc.upper()} and {toloc.upper()}"
                else:
                    for item in vec[:-1]:
                        items = items + f" {meal},"
                    items = items[:-1] + f" and {vec[-1]}"
                    message = f"We have the aircraft {items} for the flights between {fromloc.upper()} and {toloc.upper()}"
            else:
                message = f"Sorry we dont have informations about the aircrafts for the flights between {fromloc.upper()} and {toloc.upper()}"

            dispatcher.utter_message(text=message)

        else:
            dispatcher.utter_message(text='Error intent not listed')