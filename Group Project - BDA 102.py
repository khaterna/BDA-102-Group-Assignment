
# coding: utf-8

# In[6]:


# Install a pip package in the current Jupyter kernel
import sys
get_ipython().system('{sys.executable} -m pip install tweepy #Cannot use pip install tweepy because it is a conda environment. Installing tweepy')


# In[24]:


get_ipython().system('conda install --yes --prefix {sys.prefix} tweepy')


# In[26]:


get_ipython().system('conda install --yes --prefix {sys.prefix} textblob')


# In[27]:


import sys
get_ipython().system('{sys.executable} -m pip install textblob')


# In[32]:


import sys
get_ipython().system('{sys.executable} -m pip install aylien-apiclient')


# In[54]:


# Setting up libraries
import tweepy           # To consume Twitter's API
from tweepy import OAuthHandler
import pandas as pd     # To handle data
import numpy as np      # For number computing
import re
from textblob import TextBlob # To help with textual analysis
import json


# In[40]:


# Twitter App access keys for @noor

# Consume:
CONSUMER_KEY    = ''
CONSUMER_SECRET = ''

# Access:
ACCESS_TOKEN  = ''
ACCESS_SECRET = ''

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


# In[90]:


# We import our access keys:
#from credentials import *    # This will allow us to use the keys as variables

# API's setup:
def twitter_setup():
   
   ## Utility function to setup the Twitter's API
   ## with access keys provided.
    
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    #api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    api = tweepy.API(auth)
    ##status = api.user_timeline(user='sylviajruiz', count=1)[0]
    #json.dumps(status)   
    #for status in tweets:
        #json.dumps(status._json,file,sort_keys = True,indent = 4)
    return api


# In[104]:


# We create an extractor object:
extractor = twitter_setup()
#We are looking into #familiesbelongtogether whose user handle is @sylviajruiz
# We create a tweet list as follows:
tweets = extractor.user_timeline(screen_name="sylviajruiz", count=500)
print("Number of tweets extracted: {}.\n".format(len(tweets)))

# We print the most recent 10 tweets:
print("10 recent tweets:\n")
for tweet in tweets[:10]:
    print(tweet.text)
    print()


# In[105]:


#Creating a simple data frame to capture the tweets 
twitter_data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
twitter_data.head(10)


# In[106]:


#making sense of the tweets and providing context 
# We add relevant data:
twitter_data['len']  = np.array([len(tweet.text) for tweet in tweets])
twitter_data['ID']   = np.array([tweet.id for tweet in tweets])
twitter_data['Date'] = np.array([tweet.created_at for tweet in tweets])
twitter_data['Source'] = np.array([tweet.source for tweet in tweets])
twitter_data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
twitter_data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])


# In[107]:


twitter_data.head(10) #Checking dataframe 


# In[108]:


twitter_data.to_csv('twitterdata.csv')


# In[109]:


#Attempt to do the json format. Unsuccessful so far.
results = []
#Get the first 500 items based on the search query
for tweet in tweepy.Cursor(twitter_setup().search, q='%bringfamiliestogether').items(500):
    results.append(tweet)
print (len(results)) #confirming that 500 tweets were extracted 



# In[ ]:


results = []
#Get the first 500 items based on the search query
for tweet in tweepy.Cursor(twitter_setup().search, q='%bringfamiliestogether').items(500):
    results.append(tweet)
print (len(results))

