# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from urllib.request import urlopen
from rasa_sdk.events import SlotSet

import json, api


class ActionCheckWeather(Action):

    def name(self) -> Text:
        return "action_check_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            try:
                city = tracker.slots["city"]

                # ent = tracker.latest_message['entities']
                # if not ent:
                #     dispatcher.utter_message(text="You didn't give me a city. Try agian.")
                #     return []
                # else:
                #     for entity in ent:
                #         if entity['entity'] == "city":
                #             city = entity['value']
                #             break

                #         dispatcher.utter_message(text="It isn't city I guess. Try agian.")
                #         return []

            
                city = city.replace(" ", "%20")

                url = "http://api.openweathermap.org/data/2.5/weather?appid="+ api.api_key_weather +"&q="+city+"&units=metric"

                response = urlopen(url)
                data_json = json.loads(response.read())

                name = data_json['name']
                clouds = data_json['weather'][0]['description']
                temp = data_json['main']['temp']
                pressure = data_json['main']['pressure']
                
                dispatcher.utter_message(text=f"""The weather in {name} 
                 Clouds: {clouds}
                 Temperature: {temp}°C
                 Pressure: {pressure} hPa""")
            except Exception as e:
                print(e)
                dispatcher.utter_message(text="Sorry, I can not check the weather now :(")
            return [SlotSet("city", None)]
