import streamlit as st
import datetime
import requests
from geopy.geocoders import Nominatim
from geopy.distance import distance
import pandas as pd
from streamlit_folium import st_folium, folium_static
import folium


def check_bounding_box(location):
    BB_LATITUDE = [40.5, 40.9]
    BB_LONGITUDE = [-74.3, -73.7]
    """Checks if the location is within the bounding box (i.e. inside NYC)"""
    if BB_LATITUDE[0] < location.latitude < BB_LATITUDE[1] \
        and BB_LONGITUDE[0] < location.longitude < BB_LONGITUDE[1]:
            return True

    return False

'''
# :statue_of_liberty: NYC Taxi
### Estimate the cost of your taxi ride in NYC :taxi:

'''
pu_location = None
do_location = None

url = 'https://taxifare-pqttrr3oaq-ew.a.run.app/predict'

#Initialize map
m = folium.Map(location=[40.75,-73.975], zoom_start=11)


columns = st.columns(3)
columns[0].write('**:date: :clock1: When do you want a cab?**')
d = columns[0].date_input('Date', value=datetime.datetime.now())
t = columns[0].time_input('Time', value=datetime.datetime.now())

columns[1].write('**:pushpin: What\'s your journey ?**')

pu_address = columns[1].text_input('Start',placeholder="Enter address", key=1)
do_address = columns[1].text_input('Finish',placeholder="Enter address", key=2)

if pu_address != '':
    geolocator_pu = Nominatim(user_agent="pu")
    pu_location = geolocator_pu.geocode(pu_address)

    if pu_location is None:
        columns[1].write(":red[*Invalid pick-up address*]")
    elif check_bounding_box(pu_location):
        start = folium.Marker(
            [pu_location.latitude, pu_location.longitude],
            tooltip=f'Pick-up address : {pu_address}',
            icon=folium.map.Icon(color='green',icon='circle-dot',prefix='fa')
        )
        start.add_to(m)
    else:
        columns[1].write(":red[*Pick-up address out of bounds*]")

if do_address != '':
    #Convert address to geolocation
    geolocator_do = Nominatim(user_agent="do")
    do_location = geolocator_do.geocode(do_address)

    #Create Marker if address is valid or show error message
    if do_location is None:
        columns[1].write(":red[*Invalid dropoff address*]")
    elif check_bounding_box(do_location):
        end = folium.Marker(
            [do_location.latitude, do_location.longitude],
            tooltip=f'Drop-off address : {do_address}',
            icon=folium.map.Icon(color='red',icon='circle-dot',prefix='fa')
        )
        end.add_to(m)
    else:
        columns[1].write(":red[*Drop-off address out of bounds*]")

if pu_location is not None and do_location is not None :
    folium.PolyLine([[pu_location.latitude,pu_location.longitude],
                     [do_location.latitude, do_location.longitude]]).add_to(m)

columns[2].write('**:couple: How many passenger ?**')
passengers = columns[2].number_input('Number', value=1, min_value=1, max_value=5)

if pu_location is not None and do_location is not None :
        params = {
            "pickup_datetime":f'{d} {t}',
            "pickup_latitude":pu_location.latitude,
            "dropoff_latitude":do_location.latitude,
            "pickup_longitude":pu_location.longitude,
            "dropoff_longitude":do_location.longitude,
            'passenger_count':passengers
        }

        with st.spinner(text="Calculation in progress..."):
            result = requests.get(url,params)
        cost = result.json()['fare']
        st.markdown(f'#### Estimated cost : ${round(cost,2)}')
else:
    st.write(' ')

st_data = folium_static(m)

st.write('Made with ❤️ by Coralie Clot')
