
# coding: utf-8

# In[3]:


#Importing libraries 
import tweepy           # To consume Twitter's API
from tweepy import OAuthHandler
import pandas as pd     # To handle data
import numpy as np      # For number computing
import re
from textblob import TextBlob # To help with textual analysis
import json


# In[4]:


bringfamiliestogether= pd.read_csv('C:/Users/shabnaz/Documents/BDA 102/BringFamiliesTogether.csv')


# In[5]:


bringfamiliestogether.head(10) #Checking the 1st 10 rows 


# In[6]:


bringfamiliestogether['text'].head(100) #Checking column that contains the tweets


# In[7]:


#Need to clean the column "text" which contains all the tweets 
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace('\'','')#Remove the single quote
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace('\’','')#Remove the single quote ’
bringfamiliestogether['text'] = bringfamiliestogether.text.replace('\,','') #Remove the comma
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace('\@([a-zA-Z0-9]{1,15})','') #Remove the @ mark
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace('\"','') #Remove the double quote
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace('\t','') #Remove the tab character
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace('RT','') #Remove the RT character
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace('\:','') #Remove the colon
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace('\#','') #Remove the hashtag
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace(r'http\S+','') #Remove the url
#bringfamiliestogether['text'] = bringfamiliestogether['text'].apply(lambda x: re.sub('[!@#$:).;,?&_]', '', x.lower())) #Removing all addiitonal special characters
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace('!','') #Remove the ! 
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace('\n','') #Remove the \n
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace('\r','') #Remove the \r
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace('\r\n','') #Remove the \r\n
bringfamiliestogether['text'] = bringfamiliestogether.text.str.lower() #Setting all words to lowercase
bringfamiliestogether['text'] = bringfamiliestogether.text.str.replace(u'['u'\U0001F300-\U0001F64F,'u'\U0001F680-\U0001F6FF,'u'\U0001F300-\U0001F5FF,'u'\U0001F600-\U0001F64F,'u'\U0001F1E0-\U0001F1FF,'u'\U0001F600-\U0001F64F]','')




# In[8]:


print(bringfamiliestogether['text'][0:100])


# In[115]:


import sys
get_ipython().system('{sys.executable} -m pip install vaderSentiment')


# In[9]:


#Using Vader Sentimment analysis to get the polarity and sentiment of tweet 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

def print_sentiment_scores(sentence):
    snt = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(snt)))
    


# In[10]:


print_sentiment_scores(bringfamiliestogether['text'][7]) #Checking the sentiment of a tweet 


# In[11]:


#Creating a new list of items to record the sentiment of tweets 
tweet = []
ID = []
Date = []
Source = []
Likes = []
RTs= []
Location = []
compound = []
pos = []
neu = []
neg = []

for i in range(0, len(bringfamiliestogether[0:5000])):
    tweet.append(bringfamiliestogether['text'][i])
    ID.append(bringfamiliestogether['id'][i])
    Date.append(bringfamiliestogether['created_at'][i])
    Source.append(bringfamiliestogether['source'][i])
    Likes.append(bringfamiliestogether['favorite_count'][i])
    RTs.append(bringfamiliestogether['retweet_count'][i])
    Location.append(bringfamiliestogether['location'][i])
    compound.append(analyser.polarity_scores(bringfamiliestogether['text'][i])['compound'])
    pos.append(analyser.polarity_scores(bringfamiliestogether['text'][i])['pos'])
    neu.append(analyser.polarity_scores(bringfamiliestogether['text'][i])['neu'])
    neg.append(analyser.polarity_scores(bringfamiliestogether['text'][i])['neg'])


# In[13]:


#Creating a new dataframe by putting the columns back together
new_df = pd.DataFrame({'tweet' : tweet,
                          'ID' : ID,
                          'Date' : Date,
                          'Source' : Source,
                          'Likes' : Likes,
                          'RTs' : RTs,
                          'Location': Location,
                          'compound' : compound,
                          'pos' : pos,
                          'neu' : neu,
                          'neg': neg})
new_df= new_df[['tweet','ID','Date','Source','Likes','RTs','Location','compound','pos','neu','neg']]


# In[86]:


# We extract the tweet with most favorite and most retweets:

fav_max = np.max(bringfamiliestogether['favorite_count'])
rt_max  = np.max(bringfamiliestogether['retweet_count'])

fav = bringfamiliestogether[bringfamiliestogether.favorite_count == fav_max].index[0]
rt  = bringfamiliestogether[bringfamiliestogether.retweet_count == rt_max].index[0]

# most favorite:
print("The tweet with more likes is: \n{}".format(bringfamiliestogether['text'][fav]))
print("Number of likes: {}".format(fav_max))


# most retweets:
print("The tweet with more retweets is: \n{}".format(bringfamiliestogether['text'][rt]))
print("Number of retweets: {}".format(rt_max))


# In[108]:


#Doing a time graph of favorite and retweet frequency
tfav = pd.Series(data=new_df['Likes'].values, index=new_df['Date'])
tfav.plot(figsize=(16,4), label="Likes", legend=True)
tret = pd.Series(data=new_df['RTs'].values, index=new_df['Date'])
tret.plot(figsize=(16,4), label="Retweets", legend=True)


# In[14]:


# We obtain all possible sources:
sources = []
for source in new_df['Source']:
    if source not in sources:
        sources.append(source)

# We print sources list:
print("Creation of content sources:")
for source in sources:
    print("* {}".format(source))


# In[16]:


# We create a numpy vector mapped to labels:
percent = np.zeros(len(sources))

for source in new_df['Source']:
    for index in range(len(sources)):
        if source == sources[index]:
            percent[index] += 1
            pass

percent /= 100

# Pie chart:
pie_chart = pd.Series(percent, index=sources, name='Sources')
print(pie_chart.plot.pie(fontsize=11, autopct='%.2f', figsize=(6, 6)));


# In[17]:


locations = []
for location in new_df['Location']:
    if location not in locations:
        locations.append(location)

# We print sources list:
print("Creation of content locations:")
for location in locations:
    print("* {}".format(location))


# In[122]:


#20 top most locations of tweets in terms of cities
new_df['Location'].value_counts()[1:20].plot(kind='barh')


# In[19]:


#Trying to plot these city in a map with a frequency count. Having issues to install basemap and geopy
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
#from geopy.geocoders import Nominatim
import math
Frequency = new_df['Location'].map(new_df.groupby('Location').size())
cities = [new_df['Location'], Frequency]
scale = 5

map = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
        projection='lcc',lat_1=32,lat_2=45,lon_0=-95)

# load the shapefile, use the name 'states'
map.readshapefile('st99_d00', name='states', drawbounds=True)

# Get the location of each city and plot it
geolocator = Nominatim()
for (city,count) in cities:
    loc = geolocator.geocode(city)
    x, y = map(loc.longitude, loc.latitude)
    map.plot(x,y,marker='o',color='Red',markersize=int(math.sqrt(count))*scale)
plt.show()


# In[146]:


import sys
get_ipython().system('{sys.executable} -m pip install basemap #Putting the commands to install basemap.')


# In[131]:


get_ipython().system('pip install https://downloads.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz')
    

