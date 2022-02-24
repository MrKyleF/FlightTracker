#!/usr/bin/env python
# coding: utf-8

# In[1]:


from FlightRadar24.api import FlightRadar24API
fr_api = FlightRadar24API()
from time import sleep
from datetime import datetime


# In[2]:


import os 
import folium
from folium import plugins
import rioxarray as rxr
import earthpy as et
import earthpy.spatial as es


# In[3]:


#Checks for Flights above an altitude
#48,000ft and greater is typically only miltary aircraft (few private jets)
def checkForAltitudeInterest(flights, min_altitude=48000):
    flights_of_interest = []
    #Creates list of flights above min altitude
    for flight in flights:
        if flight.altitude >= min_altitude:
            flights_of_interest.append(flight)
    return flights_of_interest


# In[4]:


#Plots location on map with description
def plotInfo(flight, map_, count):
    colors = ['darkred', 'red', 'lightred', 'orange', 'darkpurple', 'purple', 'pink', 'beige', 'darkblue', 'blue', 'cadetblue', 'lightblue', 'darkgreen', 'green', 'lightgreen', 'black', 'gray', 'lightgray']
    data_string = ""
    data_string += ("Call Sign: " + flight.callsign)
    data_string += (" Altitude: " + str(flight.altitude) + " ft")
    data_string += (" Heading: " + str(flight.heading) + "")
    data_string += (" Registration: " + str(flight.registration))
    if flight.aircraft_code == "Q4":
        data_string += (" Aircraft: NORTHROP GRUMMAN RQ-4 Global Hawk")
    else:
        data_string +=  (" Aircraft Code:" + str(flight.aircraft_code))
    folium.Marker(
        location=[flight.latitude, flight.longitude], # coordinates for the marker (Earth Lab at CU Boulder)
        popup=data_string, # pop-up label for the marker
        icon=folium.Icon(color=colors[count % len(colors)],icon="plane"),
    ).add_to(map_)
    return map_


# In[ ]:


flights = fr_api.get_flights()
flights = checkForAltitudeInterest(flights)
#Create center point between all flights
lat = 0
long = 0
for flight in flights:
    lat = lat + flight.latitude
    long = long + flight.longitude
lat = lat / len(flights)
long = long / len(flights)
last_cordindats = [flights[-1].latitude, flights[-1].longitude]
#Create a single map and continue to add new locations to it
map_ = folium.Map(location=[lat, long], tiles = 'Stamen Terrain',zoom_start = 2)
count = 0
while True:
    #Grab all flights
    flights = fr_api.get_flights()
    #Filter for only high altitude
    flights = checkForAltitudeInterest(flights)
    #Plot each flight currently
    for flight in flights:
        map_ = plotInfo(flight, map_, count)
    #Get current Date and time for file name
    now = datetime.now() # current date and time
    date_time = now.strftime("%m-%d-%Y_%H:%M:%S")
    #Save the map to a directory called maps with the current data and time as file name
    map_.save("/tf/Incongruity/Flight Tracking/Maps/" + date_time + ".html")
    #Move to next color for plotting, so change can be seen between points
    count += 1
    #Wait for 30 seconds before tracking all flights again
    sleep(30)


# In[ ]:





# In[ ]:




