import tkinter as tk
import requests, base64

class OpenWeatherMap:
    APPID = '73100b5568ba54fe12fea84256637ea1'  #API key

    def __init__(self):
        self.url = "http://api.openweathermap.org/data/2.5/weather?appid={appid}&q={city}&units=metric"
        self.json = {}

    def get_city(self, city):
        url = self.url.format(appid=OpenWeatherMap.APPID, city=city)
        self.json = requests.get(url).json()
        return self.json

    def get_main(self, key):
        return self.json['main'][key]
    
    def get(self, key):
        return self.json[key]
    
    def get_sys(self, key):
        return self.json["sys"][key]
    
    def get_weather(self, key):
        return self.json['weather'][0][key]
    
   
    def get_icon_data(self):
        icon_id = self.json['weather'][0]['icon']
        url = 'http://openweathermap.org/img/wn/{icon}.png'.format(icon=icon_id)
        response = requests.get(url, stream=True)
        return base64.encodebytes(response.raw.read())            
            
class OWIconLabel(tk.Label):
    def __init__(self, parent, **kwargs):
        weather_icon = kwargs.pop('weather_icon', None)
        if weather_icon is not None:
            self.photo = tk.PhotoImage(data=weather_icon)
            kwargs['image'] = self.photo

        super().__init__(parent, **kwargs)