import streamlit as st
import datetime
import requests


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
columns[0].write('**:pushpin: Pickup location**')
pu_lat = columns[1].number_input('Latitude',value=-73.950655,format='%f', step=0.000001)
pu_lon = columns[1].number_input('Longitude',value=40.783282,format='%f',step=0.000001)
#pu_address = columns[1].text_input('Enter Address','',key=1)

columns = st.columns(2)
columns[0].write('**:pushpin: Dropoff location**')
do_lat = columns[1].number_input('Latitude',value=-73.984365,format='%f',step=0.000001)
do_lon = columns[1].number_input('Longitude',value=40.769802, format='%f',step=0.000001)
#do_address = columns[1].text_input('Enter Address','',key=2)

columns = st.columns(2)
columns[0].write('**:couple: Passengers**')
passengers = columns[1].number_input('Number', value=1, min_value=1, max_value=5)

# def get_location(address:str)->tuple:
#     url_geo = "https://nominatim.openstreetmap.org/search"
#     params_geo= {"q":address, "format":"json"}
#     response = requests.get(url_geo, params = params_geo)
#     st.write(response.status_code)
#     if response.status_code > 299 :
#         return None
#     return response.json()[0]["lat"], response.json()[0]["lon"]






if st.button('Get fare'):

    # pu = get_location(pu_address)
    # do = get_location(do_address)


    # if pu is not None and do is not None :

        params = {
            "pickup_datetime":f'{d} {t}',
            "pickup_latitude":pu_lat,
            "dropoff_latitude":do_lat,
            "pickup_longitude":pu_lon,
            "dropoff_longitude":do_lon,
            'passenger_count':passengers
        }

        result = requests.get(url,params)
        cost = result.json()['fare']
        st.write(f'**Estimated cost : ${round(cost,2)}**')
        # df = pd.DataFrame([[pu_lat,pu_lon],[do_lat,do_lon]], columns=['lat','lon'])
        # st.map(df)

    # elif pu is None and do is None :
    #     st.write("Invalid pick-up and drop-off addresses")
    # elif pu is None :
    #     st.write("Invalid pick-up address")
    # else :
    #     st.write("Invalid drop-off address")
