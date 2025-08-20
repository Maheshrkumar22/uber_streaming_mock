import streamlit as st
from configparser import ConfigParser
import pandas as pd
import mysql.connector
import folium
from streamlit_folium import folium_static
from datetime import timedelta
import time

config = ConfigParser()
config.read('config.ini')

conn = mysql.connector.connect(
    host='localhost',
    user=config['db']['user_name'],
    password=config['db']['password'],
    database='uber_db'
)

def get_data():
    cur = conn.cursor()
    cur.execute("SELECT zone, COUNT(*) as count FROM bookings WHERE timestamp > NOW() - INTERVAL 5 MINUTE GROUP BY zone")
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=['zone', 'count'])
    cur.close()
    return df

st.title('Uber Mock Dashboard')

zone_coords = {
    'Downtown': [10.974814,79.396773],
    'Suburb': [10.963922, 79.392213],
    'Airport': [37.6213, -122.3790],
    'Uptown': [37.8044, -122.4110]
}

while True:
    df = get_data()
    if not df.empty:
        st.subheader('Bookings per Zone (Last 5 Min)')
        st.bar_chart(df.set_index('zone')['count'])
        
        m = folium.Map(location=[10.974814,79.396773], zoom_start=12)
        for _, row in df.iterrows():
            zone = row['zone']
            if zone in zone_coords:
                folium.Marker(zone_coords[zone], popup=f"{zone}: {row['count']}").add_to(m)
        folium_static(m)
    
    time.sleep(10)
    st.rerun()