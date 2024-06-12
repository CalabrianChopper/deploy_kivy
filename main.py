
#**********************************
# Developed by QMT 2024
#**********************************

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
import requests
import json

#**********************************
# Metodo di ricezione dati
#**********************************

def update_data(dt=None):
    try:
        response = requests.get("http://192.168.4.1/GET/get_sensor_data")
        data = response.json()
        app.temperature_label.text = f"Temperatura: {data['temperature']} °C"
        app.humidity_label.text = f"Umidità: {data['humidity']} %"
        pump_state = int(data['pump_state'])
        app.pump_state_label.text = f"Pompa: {'Accesa' if pump_state == 1 else 'Spenta'}"
        app.pump_icon.source = 'green_circle.png' if pump_state == 1 else 'red_circle.png'
        app.pump_duration = data['pump_duration']
        app.pause_duration = data['pause_duration']
        app.pump_duration_label.text = f"Durata Pompa: {data['pump_duration']} min"
        app.pause_duration_label.text = f"Durata Pausa: {data['pause_duration']} min"
        app.temperature_bar.value = data['temperature'] + 20  
        app.humidity_bar.value = data['humidity']
    except requests.exceptions.RequestException as e:
        print("Errore durante l'aggiornamento dei dati:", e)
        
#**********************************
# Metodi di settaggio della pompa 
#**********************************
        
def increment_pump_duration(instance):
    new_duration = app.pump_duration + 1
    set_pump_duration(new_duration)

def decrement_pump_duration(instance):
    if app.pump_duration > 1:
        new_duration = app.pump_duration - 1
    else:
        new_duration = app.pump_duration
    set_pump_duration(new_duration)

def increment_pause_duration(instance):
    new_pause = app.pause_duration + 1
    set_pause_duration(new_pause)

def decrement_pause_duration(instance):
    if app.pause_duration > 1:
        new_pause = app.pause_duration - 1
    else:
        new_pause = app.pause_duration
    set_pause_duration(new_pause)

def set_pump_duration(new_duration):
    try:
        url = f"http://192.168.4.1/SET/set_pump_duration?duration={new_duration}"
        response = requests.get(url)
        if response.status_code == 200:
            app.pump_duration = new_duration
            app.pump_duration_label.text = f"Durata Pompa: {new_duration} min"
            print("Durata della pompa aggiornata con successo.")
        else:
            print("Errore durante l'aggiornamento della durata della pompa.")
    except requests.exceptions.RequestException as e:
        print("Errore durante l'aggiornamento della durata della pompa:", e)

def set_pause_duration(new_pause):
    try:
        url = f"http://192.168.4.1/SET/set_pause_duration?pause={new_pause}"
        response = requests.get(url)
        if response.status_code == 200:
            app.pause_duration = new_pause
            app.pause_duration_label.text = f"Durata Pausa: {new_pause} min"
            print("Durata della pausa aggiornata con successo.")
        else:
            print("Errore durante l'aggiornamento della durata della pausa.")
    except requests.exceptions.RequestException as e:
        print("Errore durante l'aggiornamento della durata della pausa:", e)

#**********************************
# Main del software
#**********************************

class pumpControlApp(App):
    pump_duration = NumericProperty(10)
    pause_duration = NumericProperty(30)

    def build(self):
        global app
        app = self

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.temperature_label = Label(text="Temperatura: -- °C")
        layout.add_widget(self.temperature_label)

        self.temperature_bar = ProgressBar(max=70, value=0)  
        layout.add_widget(self.temperature_bar)

        self.humidity_label = Label(text="Umidità: -- %")
        layout.add_widget(self.humidity_label)

        self.humidity_bar = ProgressBar(max=100, value=0)  
        layout.add_widget(self.humidity_bar)

        self.pump_state_label = Label(text="Pompa: --")
        layout.add_widget(self.pump_state_label)
        
        self.pump_icon = Image(source='red_circle.png')
        layout.add_widget(self.pump_icon)

        update_button = Button(text="Aggiorna Dati")
        update_button.bind(on_press=update_data)
        layout.add_widget(update_button)
        
        # Durata Pompa
        pump_duration_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        self.pump_duration_label = Label(text="Durata Pompa: -- min")
        pump_duration_layout.add_widget(Button(text="-", on_press=decrement_pump_duration))
        pump_duration_layout.add_widget(self.pump_duration_label)
        pump_duration_layout.add_widget(Button(text="+", on_press=increment_pump_duration))
        layout.add_widget(pump_duration_layout)

        # Durata Pausa
        pause_duration_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        self.pause_duration_label = Label(text="Durata Pausa: -- min")
        pause_duration_layout.add_widget(Button(text="-", on_press=decrement_pause_duration))
        pause_duration_layout.add_widget(self.pause_duration_label)
        pause_duration_layout.add_widget(Button(text="+", on_press=increment_pause_duration))
        layout.add_widget(pause_duration_layout)

        Clock.schedule_once(update_data, 3)
        Clock.schedule_interval(update_data, 30)

        return layout

if __name__ == '__main__':
    pumpControlApp().run()