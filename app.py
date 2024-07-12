import streamlit as st
import datetime
import requests
from geopy.geocoders import Nominatim
import pandas as pd

'''
# :statue_of_liberty: NYC Taxi
### Estimate the cost of your taxi ride in NYC :taxi:

'''

url = 'https://taxifare.lewagon.ai/predict'

columns = st.columns(2)
columns[0].write('**:date: :clock1: Pickup date & time**')
d = columns[1].date_input('Date', value=datetime.date(2014, 7, 6))
t = columns[1].time_input('Time', value=datetime.time(19,18,00))


columns = st.columns(2)
columns[0].write('**:pushpin: Pick-up Address**')
#pu_lat = columns[1].number_input('Latitude',value=-73.950655,format='%f', step=0.000001)
#pu_lon = columns[1].number_input('Longitude',value=40.783282,format='%f',step=0.000001)
pu_address = columns[1].text_input('Enter Address',value='Central Park',key=1)

columns = st.columns(2)
columns[0].write('**:pushpin: Drop-off Address**')
#do_lat = columns[1].number_input('Latitude',value=-73.984365,format='%f',step=0.000001)
#do_lon = columns[1].number_input('Longitude',value=40.769802, format='%f',step=0.000001)
do_address = columns[1].text_input('Enter Address',value='Empire State Building',key=2)

columns = st.columns(2)
columns[0].write('**:couple: Passengers**')
passengers = columns[1].number_input('Number', value=1, min_value=1, max_value=5)

if st.button('Get fare'):

    geolocator_pu = Nominatim(user_agent="pu")
    geolocator_do = Nominatim(user_agent="do")

    pu_location = geolocator_pu.geocode(pu_address)
    do_location = geolocator_do.geocode(do_address)

    if pu_location is not None and do_location is not None :
        params = {
            "pickup_datetime":f'{d} {t}',
            "pickup_latitude":pu_location.latitude,
            "dropoff_latitude":do_location.latitude,
            "pickup_longitude":pu_location.longitude,
            "dropoff_longitude":do_location.longitude,
            'passenger_count':passengers
        }

        result = requests.get(url,params)
        cost = result.json()['fare']
        st.write(f'**Estimated cost : ${round(cost,2)}**')
        df = pd.DataFrame([[pu_location.latitude,pu_location.longitude],[do_location.latitude,do_location.longitude]], columns=['lat','lon'])
        st.map(df)

    elif pu_location is None and do_location is None :
        st.write("Invalid pick-up and drop-off addresses")
    elif pu_location is None :
        st.write("Invalid pick-up address")
    else :
        st.write("Invalid drop-off address")
