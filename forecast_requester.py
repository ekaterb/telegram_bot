import requests
import yaml
import logging


#TODO add logging

def get_coodinates(city):
    with open('cities_config.yaml') as yamlfile:
        cities = yaml.safe_load(yamlfile)
    return cities[city]


def get_forecast(city):
    coordinates = get_coodinates(city)
    daily_params = ["temperature_2m_max", "apparent_temperature_max", "uv_index_max", "precipitation_sum", "rain_sum",
                    "snowfall_sum", "windspeed_10m_max"]  # TODO move to config
    keys = "daily=" + ",".join(x for x in daily_params) + f"&timezone={coordinates['timezone']}"
    url = "https://api.open-meteo.com"  # TODO move to env var
    path = f"/v1/forecast?latitude={coordinates['latitude']}&longitude={coordinates['longitude']}&{keys}"
    response = requests.get(url=url + path, verify=False)
    # TODO add errors pr
    return response.json()


class WeaterHandler:
    def __init__(self, weather_data):
        self.weather_data = weather_data
        with open('cat_config.yaml') as yamlfile:
            self.evaluation = yaml.safe_load(yamlfile)

    def check_for_temperature(self):
        """
        Check and evaluate daily temperature in °C
        :return: temperature, evaluation (from cat_config.yaml)
        """
        temperature = self.weather_data['daily']['temperature_2m_max'][0]  # units - °C
        result = None
        for i in self.evaluation['temperature'].keys():
            if temperature >= i:
                result = self.evaluation['temperature'][i]
        return temperature, result

    def check_for_rain(self):
        """
        Check and evaluate number of mm from rain
        :return: rains evaluation (from cat_config.yaml)
        """
        rain_sum = self.weather_data['daily']['rain_sum'][0]  # units - mm
        result = None
        for i in self.evaluation['rain'].keys():
            if rain_sum >= i:
                result = self.evaluation['rain'][i]
        return result

    def check_windspeed_max(self):
        windspeed_max = self.weather_data['daily']['windspeed_10m_max'][0]  # units - km/h
        result = None
        for i in self.evaluation['windspeed'].keys():
            if windspeed_max >= i:
                result = self.evaluation['windspeed'][i]
        return result

    def check_for_snowfall(self):
        """
        Check if expects show
        :return: snow if expext, else no_snow
        """
        result = "no_snow"
        snowfall_sum = self.weather_data['daily']['snowfall_sum'][0]  # units - cm
        if snowfall_sum > 0:
            result = "snow"
        return result

    def check_uv_index_max(self):
        """
        Get max UV index for the day
        :return: uv_index_max
        """
        uv_index_max = self.weather_data['daily']['uv_index_max'][0]  # units - uv index
        return uv_index_max

    def get_overall_evaluation(self):
        temp_degrees, temperature = self.check_for_temperature()
        # TODO reconsider the output
        return {
            "temperature": temperature,
            "temp_degrees": temp_degrees,
            "rain": self.check_for_rain(),
            "windspeed": self.check_windspeed_max(),
            "snowfall": self.check_for_snowfall(),
            "uv_index": self.check_uv_index_max()
        }

# picture_path = f"pictures/{r['temperature']}_{r['rain']}_{r['snowfall']}_{r['windspeed']}"
