import json
import pprint

f = open('teste.json')

data = json.load(f)

entities = ['airline_name',
'flight_number',
'depart_time.time_relative',
'arrive_time.time_relative',
'depart_time.end_time',
'flight_mod',
'fare_basis_code',
'depart_date.today_relative',
'arrive_time.end_time',
'fromloc.airport_name',
'or',
'depart_time.period_of_day',
'arrive_date.day_name',
'day_name',
'time_relative',
'fare_amount',
'airline_code',
'depart_date.date_relative',
'toloc.state_code',
'depart_date.day_number',
'cost_relative',
'round_trip',
'fromloc.city_name',
'fromloc.state_code',
'arrive_time.time',
'depart_date.month_name',
'stoploc.city_name',
'aircraft_code',
'meal',
'meal_description',
'connect',
'city_name',
'depart_time.time',
'toloc.city_name',
'flight_stop',
'depart_date.day_name',
'class_type',
'today_relative',
'arrive_date.month_name',
'date',
'city',
'airport_name']

intents = [
'greet',
'goodbye',
'affirm',
'deny',
'city',
'airline',
'ground_service',
'restriction',
'airport',
'flight',
'meal',
'quantity',
'airfare',
'distance',
'capacity',
'aircraft',
'ground_fare']

data['rasa_nlu_data']['common_examples'] = [x for x in data['rasa_nlu_data']['common_examples'] if x['intent'] in intents]
for x in range(len(data['rasa_nlu_data']['common_examples'])):
    data['rasa_nlu_data']['common_examples'][x]['entities'] = [y for y in data['rasa_nlu_data']['common_examples'][x]['entities'] if y['entity'] in entities]



aiaiIntent = set()
aiaiEntities = set()

for x in data['rasa_nlu_data']['common_examples']:
    aiaiIntent.add(x['intent'])
    for entity in x['entities']:
        aiaiEntities.add(entity['entity'])

f = open('testeSaida.json', 'w')

a = json.dumps(data, indent = 4)

f.write(a)