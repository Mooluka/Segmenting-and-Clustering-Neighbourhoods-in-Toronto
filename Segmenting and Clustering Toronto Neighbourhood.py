#!/usr/bin/env python
# coding: utf-8

# ## Segmenting and Clustering  Neighbourhoods in Toronto
# 
# The project includes scraping the Wikipedia page for the postal codes of Canada and then process and clean the data for the clustering. The clustering is carried out by K Means and the clusters are plotted using the Folium Library. The Boroughs containing the name 'Toronto' in it are first plotted and then clustered and plotted again.
# 
# All the 3 tasks of web scraping, cleaning and clustering are implemented in the same notebook for the ease of evaluation. Installing and Importing the required Libraries

# ### Week 3 Assignment

# ## Part 1 
# This includes number 1 to 8 is otaining Data from wikipedia and Geospatial link for making a data Frame consisting of Postal Codes, Borough, Neighborhood, Latitudes and longitudes

# ### 1. Import the neccessary libraries

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


# ### 3. Explore the scraped data 

# ##### Find the table containing Toronto Neighbourhood

# In[3]:


table_content=soup.find_all('table')


# ##### Find the Toronto postcodes in the table

# In[4]:


postcodes=soup.find_all('b')


# ##### Find the rows of the table

# In[5]:


rows=soup.find_all('tr')


# ##### View the links in the scraped data

# In[6]:


links=soup.find_all('a')


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


# ### 5. Build a Pandas DataFrame
# 

# In[8]:


df=pd.DataFrame(table_contents)
df['Borough']=df['Borough'].replace({'Downtown TorontoStn A PO Boxes25 The Esplanade':'Downtown Toronto Stn A',
                                             'East TorontoBusiness reply mail Processing Centre969 Eastern':'East Toronto Business',
                                             'EtobicokeNorthwest':'Etobicoke Northwest','East YorkEast Toronto':'East York/East Toronto',
                                             'MississaugaCanada Post Gateway Processing Centre':'Mississauga'})
df[0:11]


# ### 6. Import Toronto Geospatial Data 
# 
# I will scrap the Cousera page and obtain a link to Geospatial Data

# link to required geospatial data is:
# https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/labs_v1/Geospatial_Coordinates.csv

# #### find the Table

# In[9]:


get_ipython().system("wget -q -O 'Geospatial_Coordinates.csv' https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/labs/newyork_data.csv")
print('Data downloaded!')


# ### 7. import the geospatial data into a pandas dataframe

# In[10]:


dfg=pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/labs_v1/Geospatial_Coordinates.csv')
dfg.head()


# ##### Rename PostalCode columns to Postcode for merging the tables

# In[11]:


df.rename(columns={'PostalCode': 'Postal Code'}, inplace=True)
df.head()


# ### 8.Merge the df and dfg tables to form Toronto_table with geospatial coordinates

# In[12]:


Toronto_table=pd.merge(df,dfg,on=['Postal Code'])
Toronto_table[:20]


# ###  View the Boroughs and Count Borough and Neighborhoods

# In[13]:


#display the Borough in toronto
Toronto_table['Borough'].unique()


# In[14]:


print('The dataframe has {} boroughs and {} neighborhoods.'.format(
        len(Toronto_table['Borough'].unique()),
        Toronto_table.shape[0]))


# ## Part2  
# #### Map of Toronto showing the Neighborhoods
# #### geopy library to get the latitude and longitude values of Toronto City.
# In order to define an instance of the geocoder, we need to define a user_agent. We will name our agent <em>T_explorer</em>, as shown below.

# In[15]:


# find the coordinates of toronto 
address = 'Toronto'

geolocator = Nominatim(user_agent="T_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto City are {}, {}.'.format(latitude, longitude))


# #### Create a map of Toronto with neighborhoods superimposed on top.

# In[16]:


# create map of Toronto using latitude and longitude values
map_Toronto = folium.Map(location=[latitude, longitude], zoom_start=11)

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


# ### consider the Downtown Toronto

# In[17]:


Downtowntoronto_data=Toronto_table[Toronto_table['Borough'] == 'Downtown Toronto'].reset_index(drop=True)
Downtowntoronto_data.head()


# #### Get the geographic coordinates of Downtown Toronto 

# In[18]:


address = 'Downtown Toronto'

geolocator = Nominatim(user_agent="ny_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Downtown Toronto are {}, {}.'.format(latitude, longitude))


# #### visualizat Manhattan the neighborhoods

# In[19]:


# create map of Downtown Toronto using latitude and longitude values
map_DowntownToronto = folium.Map(location=[latitude, longitude], zoom_start=14)

# add markers to map
for lat, lng, label in zip(Downtowntoronto_data['Latitude'], Downtowntoronto_data['Longitude'], Downtowntoronto_data['Neighborhood']):
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_DowntownToronto)  
    
map_DowntownToronto


# ### Utilizing the Foursquare API to explore the neighborhoods and segment them.

# #### Define Foursquare Credentials and Version

# In[20]:


CLIENT_ID = 'LLWJJTHUBB3DCXTCXRFHDRJSTL0LZKOEKXMOGGLTRUHPQYZR' # your Foursquare ID
CLIENT_SECRET = 'Y4M2MIKQD0HNEPDVXJPLT4RIXLWBGNRTFXP2W4PME4DQ3FRF' # your Foursquare Secret
VERSION = '20180605' # Foursquare API version
LIMIT = 100 # A default Foursquare API limit value

print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# #### Let's explore the first neighborhood in our dataframe.

# Get the neighborhood's name.

# In[21]:


Downtowntoronto_data.loc[0, 'Neighborhood']


# Get the neighborhood's latitude and longitude values

# In[22]:


neighborhood_latitude = Downtowntoronto_data.loc[0, 'Latitude'] # neighborhood latitude value
neighborhood_longitude =Downtowntoronto_data.loc[0, 'Longitude'] # neighborhood longitude value

neighborhood_name = Downtowntoronto_data.loc[0, 'Neighborhood'] # neighborhood name

print('Latitude and longitude values of {} are {}, {}.'.format(neighborhood_name, 
                                                               neighborhood_latitude, 
                                                               neighborhood_longitude))


# #### Now, let's get the top 100 venues that are in Marble Hill within a radius of 500 meters.

# First, let's create the GET request URL. Name your URL **url**.

# In[23]:


# type your answer here
LIMIT = 100 # limit of number of venues returned by Foursquare API

radius = 500 # define radius
# create URL
url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
    CLIENT_ID, 
    CLIENT_SECRET, 
    VERSION, 
    neighborhood_latitude, 
    neighborhood_longitude, 
    radius, 
    LIMIT)
url # display URL


# Send the GET request and examine the resutls

# In[24]:


results = requests.get(url).json()
results


# In[25]:


# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']


# Clean the json and structure it into a pandas dataframe

# In[26]:


venues = results['response']['groups'][0]['items']
    
nearby_venues = json_normalize(venues) # flatten JSON

# filter columns
filtered_columns = ['venue.name', 'venue.categories', 'venue.location.lat', 'venue.location.lng']
nearby_venues =nearby_venues.loc[:, filtered_columns]

# filter the category for each row
nearby_venues['venue.categories'] = nearby_venues.apply(get_category_type, axis=1)

# clean columns

nearby_venues.columns = [col.split(".")[-1] for col in nearby_venues.columns]
nearby_venues.head()


# Number of venues were returned by Foursquare?
# 

# ## 2. Explore Neighborhoods in Downtown Toronto

# #### Create a function to repeat the same process to all the neighborhoods in Downtown Toronto

# In[27]:


def getNearbyVenues(names, latitudes, longitudes, radius=500):
    
    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):
        print(name)
            
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            LIMIT)
            
        # make the GET request
        results = requests.get(url).json()["response"]['groups'][0]['items']
        
        # return only relevant information for each nearby venue
        venues_list.append([(
            name, 
            lat, 
            lng, 
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Neighborhood', 
                  'Neighborhood Latitude', 
                  'Neighborhood Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearby_venues)


# #### Now write the code to run the above function on each neighborhood and create a new dataframe called _downtowntoronto_venues_.
# 

# In[28]:


# type your answer here
downtowntoronto_venues = getNearbyVenues(names=Downtowntoronto_data['Neighborhood'],
                                   latitudes=Downtowntoronto_data['Latitude'],
                                   longitudes=Downtowntoronto_data['Longitude']
                                  )


# In[29]:


print(downtowntoronto_venues.shape)
downtowntoronto_venues.head()


# check how many venues were returned for each neighborhood

# In[30]:


downtowntoronto_venues.groupby('Neighborhood').count()


# #### find out how many unique categories can be curated from all the returned venues

# In[31]:


print('There are {} uniques categories.'.format(len(downtowntoronto_venues['Venue Category'].unique())))


# ## 3. Analyze Each Neighborhood
# 

# In[32]:


# one hot encoding
downtowntoronto_onehot = pd.get_dummies(downtowntoronto_venues[['Venue Category']], prefix="", prefix_sep="")

# add neighborhood column back to dataframe
downtowntoronto_onehot['Neighborhood'] = downtowntoronto_venues['Neighborhood'] 

# move neighborhood column to the first column
fixed_columns = [downtowntoronto_onehot.columns[-1]] + list(downtowntoronto_onehot.columns[:-1])
downtowntoronto_onehot = downtowntoronto_onehot[fixed_columns]

downtowntoronto_onehot.head()


# examine the new dataframe size.

# In[33]:


downtowntoronto_onehot.shape


# #### group rows by neighborhood and by taking the mean of the frequency of occurrence of each category
# 

# In[35]:


downtowntoronto_grouped = downtowntoronto_onehot.groupby('Neighborhood').mean().reset_index()
downtowntoronto_grouped


# #### Print each neighborhood along with the top 5 most common venues
# 

# In[36]:


num_top_venues = 5

for hood in downtowntoronto_grouped['Neighborhood']:
    print("----"+hood+"----")
    temp = downtowntoronto_grouped[downtowntoronto_grouped['Neighborhood'] == hood].T.reset_index()
    temp.columns = ['venue','freq']
    temp = temp.iloc[1:]
    temp['freq'] = temp['freq'].astype(float)
    temp = temp.round({'freq': 2})
    print(temp.sort_values('freq', ascending=False).reset_index(drop=True).head(num_top_venues))
    print('\n')


# #### Put that into a _pandas_ dataframe

# Write a function to sort the venues in descending order.

# In[37]:


def return_most_common_venues(row, num_top_venues):
    row_categories = row.iloc[1:]
    row_categories_sorted = row_categories.sort_values(ascending=False)
    
    return row_categories_sorted.index.values[0:num_top_venues]


# create the new dataframe and display the top 10 venues for each neighborhood.

# In[38]:


num_top_venues = 10

indicators = ['st', 'nd', 'rd']

# create columns according to number of top venues
columns = ['Neighborhood']
for ind in np.arange(num_top_venues):
    try:
        columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
    except:
        columns.append('{}th Most Common Venue'.format(ind+1))

# create a new dataframe
neighborhoods_venues_sorted = pd.DataFrame(columns=columns)
neighborhoods_venues_sorted['Neighborhood'] = downtowntoronto_grouped['Neighborhood']

for ind in np.arange(downtowntoronto_grouped.shape[0]):
    neighborhoods_venues_sorted.iloc[ind, 1:] = return_most_common_venues(downtowntoronto_grouped.iloc[ind, :], num_top_venues)

neighborhoods_venues_sorted[0:10]


# ### 4. Cluster Neighborhoodsdowntowntoronto

# Run _k_-means to cluster the neighborhood into 5 clusters.
# 

# In[39]:


# set number of clusters
kclusters = 5

downtowntoronto_grouped_clustering = downtowntoronto_grouped.drop('Neighborhood', 1)

# run k-means clustering
kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(downtowntoronto_grouped_clustering)

# check cluster labels generated for each row in the dataframe
kmeans.labels_[0:10] 


# create a new dataframe that includes the cluster as well as the top 10 venues for each neighborhood.

# In[40]:


# add clustering labels
neighborhoods_venues_sorted.insert(0, 'Cluster Labels', kmeans.labels_)

downtowntoronto_merged = Downtowntoronto_data

# merge manhattan_grouped with manhattan_data to add latitude/longitude for each neighborhood
downtowntoronto_merged = downtowntoronto_merged.join(neighborhoods_venues_sorted.set_index('Neighborhood'), on='Neighborhood')

downtowntoronto_merged.head() # check the last columns!


# Visualize the resulting clusters

# In[41]:


# create map
map_clusters = folium.Map(location=[latitude, longitude], zoom_start=14)

# set color scheme for the clusters
x = np.arange(kclusters)
ys = [i + x + (i*x)**2 for i in range(kclusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(downtowntoronto_merged['Latitude'], downtowntoronto_merged['Longitude'], downtowntoronto_merged['Neighborhood'], downtowntoronto_merged['Cluster Labels']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(map_clusters)
       
map_clusters


# ### 5. Examine Clusters

# In[42]:


downtowntoronto_merged.loc[downtowntoronto_merged['Cluster Labels'] == 0, downtowntoronto_merged.columns[[1] + list(range(5, downtowntoronto_merged.shape[1]))]]


# #### Cluster 2

# In[43]:


downtowntoronto_merged.loc[downtowntoronto_merged['Cluster Labels'] == 1, downtowntoronto_merged.columns[[1] + list(range(5, downtowntoronto_merged.shape[1]))]]


# #### Cluster 3

# In[44]:


downtowntoronto_merged.loc[downtowntoronto_merged['Cluster Labels'] == 2, downtowntoronto_merged.columns[[1] + list(range(5, downtowntoronto_merged.shape[1]))]]


# #### Cluster 4

# In[45]:


downtowntoronto_merged.loc[downtowntoronto_merged['Cluster Labels'] == 3, downtowntoronto_merged.columns[[1] + list(range(5, downtowntoronto_merged.shape[1]))]]


# #### Cluster 5

# In[46]:


downtowntoronto_merged.loc[downtowntoronto_merged['Cluster Labels'] == 4, downtowntoronto_merged.columns[[1] + list(range(5, downtowntoronto_merged.shape[1]))]]


# In[ ]:




