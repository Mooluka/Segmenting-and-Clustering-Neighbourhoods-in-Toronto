#!/usr/bin/env python
# coding: utf-8

# ## Segmenting and Clustering Neighbourhoods in Toronto
# The project includes scraping the Wikipedia page for the postal codes of Canada and then process and clean the data for the clustering. The clustering is carried out by K Means and the clusters are plotted using the Folium Library. The Boroughs containing the name 'Toronto' in it are first plotted and then clustered and plotted again.
# 
# All the 3 tasks of web scraping, cleaning and clustering are implemented in the same notebook for the ease of evaluation.
# Installing and Importing the required Libraries

# ### Week 3 Assignment

# ## Part 1 
# This includes number 1 to 8 is otaining Data from wikipedia and Geospatial link for making a data Frame consisting of Postal Codes, Borough, Neighborhood, Latitudes and longitudes

# ### 1. importing required libraries

# In[1]:


get_ipython().system('pip install beautifulsoup4')
get_ipython().system('pip install lxml')
import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

get_ipython().system('conda install -c conda-forge geopy --yes ')
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 


from IPython.display import display_html
import pandas as pd
import numpy as np
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium # plotting library
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
import matplotlib.cm as cm
import matplotlib.colors as colors

print('Folium installed')
print('Libraries imported.')


# ### 2. Scrap wikipedia Toronto Neighborhood webpage using BeautifulSoup

# In[2]:


url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")

print(soup.prettify())


# ### 3. Explore the scraped data 

# ##### Find the table containing Toronto Neighbourhood

# In[3]:


table_content=soup.find_all('table')
table_content


# ##### Find the Toronto postcodes in the table

# In[4]:


postcodes=soup.find_all('b')
print(postcodes)


# ##### Find the rows of the table

# In[5]:


rows=soup.find_all('tr')
rows


# ##### View the links in the scraped data

# In[6]:


links=soup.find_all('a')
links


# ### 4. Convert the Scraped table_content into a list

# In[7]:


table_contents=[]
table=soup.find('table')
for row in table.findAll('td'):
    cell = {}
    if row.span.text=='Not assigned':
        pass
    else:
        cell['PostalCode'] = row.p.text[:3]
        cell['Borough'] = (row.span.text).split('(')[0]
        cell['Neighborhood'] = (((((row.span.text).split('(')[1]).strip(')')).replace(' /',',')).replace(')',' ')).strip(' ')
        table_contents.append(cell)

print(table_contents)


# ### 5. Build a Pandas DataFrame

# In[20]:


df=pd.DataFrame(table_contents)
df['Borough']=df['Borough'].replace({'Downtown TorontoStn A PO Boxes25 The Esplanade':'Downtown Toronto Stn A',
                                             'East TorontoBusiness reply mail Processing Centre969 Eastern':'East Toronto Business',
                                             'EtobicokeNorthwest':'Etobicoke Northwest','East YorkEast Toronto':'East York/East Toronto',
                                             'MississaugaCanada Post Gateway Processing Centre':'Mississauga'})
df[0:11]


# ### 6. Import Toronto Geospatial Data 
# 
# I will scrap the Cousera page and obtain a link to Geospatial Data

# In[9]:


url2="https://www.coursera.org/learn/applied-data-science-capstone/peer/I1bDq/segmenting-and-clustering-neighborhoods-in-toronto/submit"
req1 = requests.get(url2)
soup1 = BeautifulSoup(req1.text, "html.parser")
print(soup1.prettify())


# link to required geospatial data is:
# https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/labs_v1/Geospatial_Coordinates.csv

# #### find the Table

# In[10]:


get_ipython().system("wget -q -O 'Geospatial_Coordinates.csv' https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/labs/newyork_data.csv")
print('Data downloaded!')


# ### 7. import the geospatial data into a pandas dataframe

# In[11]:


dfg=pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/labs_v1/Geospatial_Coordinates.csv')
dfg.head()


# ##### Rename PostalCode columns to Postcode for merging the tables

# In[12]:


df.rename(columns={'PostalCode': 'Postal Code'}, inplace=True)
df.head()


# ### 8.Merge the df and dfg tables to form Toronto_table with geospatial coordinates

# In[13]:


Toronto_table=pd.merge(df,dfg,on=['Postal Code'])
Toronto_table[:20]


# ###  View the Boroughs and Count Borough and Neighborhoods

# In[14]:


#display the Borough in toronto
Toronto_table['Borough'].unique()


# In[15]:


print('The dataframe has {} boroughs and {} neighborhoods.'.format(
        len(Toronto_table['Borough'].unique()),
        Toronto_table.shape[0]))


# ## Part2  
# #### Map of Toronto showing the Neighborhoods
# #### geopy library to get the latitude and longitude values of Toronto City.
# In order to define an instance of the geocoder, we need to define a user_agent. We will name our agent <em>T_explorer</em>, as shown below.

# In[16]:


# find the coordinates of toronto 
address = 'Toronto'

geolocator = Nominatim(user_agent="T_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto City are {}, {}.'.format(latitude, longitude))


# #### Create a map of Toronto with neighborhoods superimposed on top.

# In[17]:


# create map of Toronto using latitude and longitude values
map_Toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, Borough, Neighborhood in zip(Toronto_table['Latitude'], Toronto_table['Longitude'], Toronto_table['Borough'], Toronto_table['Neighborhood']):
    label = '{}, {}'.format(Neighborhood, Borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_Toronto)  
    
map_Toronto


# In[ ]:





# In[ ]:




