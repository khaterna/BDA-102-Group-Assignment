
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


# In[254]:


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
CONSUMER_KEY    = 'uroQ5L1xn5tY1jh6HxEQYHMlK'
CONSUMER_SECRET = 'fNHc2yMmZRk4RwFSL6c7JG8texSfnMLgAF4Y5pddPkv9ea2mrs'

# Access:
ACCESS_TOKEN  = '1010197135852277761-zq8ZHGsu6DqoSUMjoqyJgj8YWTIQD1'
ACCESS_SECRET = 'WVe1Oe3CbU0TrfyZNwVmdtTu4oyE41S0F6g7pliZoOIew'

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


# In[204]:


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


# In[206]:


#Creating a simple data frame to capture the tweets 
twitter_data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
twitter_data.head(10)
type(twitter_data)


# In[207]:


#making sense of the tweets and providing context 
# We add relevant data:
twitter_data['len']  = np.array([len(tweet.text) for tweet in tweets])
twitter_data['ID']   = np.array([tweet.id for tweet in tweets])
twitter_data['Date'] = np.array([tweet.created_at for tweet in tweets])
twitter_data['Source'] = np.array([tweet.source for tweet in tweets])
twitter_data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
twitter_data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])


# In[208]:


twitter_data.head(10) #Checking dataframe 
#twitter_data=(twitter_data.to_string())


# In[271]:


twitter_data.to_csv('twitterdata.csv',index=False)


# In[199]:


#Attempt to do the json format. Unsuccessful so far.
#results = []
#Get the first 500 items based on the search query
#for tweet in tweepy.Cursor(twitter_setup().search, q='%bringfamiliestogether').items(500):
#    results.append(tweet)
#print (len(results)) #confirming that 500 tweets were extracted 



# In[365]:


twitter_datadf= pd.read_csv('C:/Users/shabnaz/twitterdata.csv')


# In[366]:


twitter_datadf.head(10)


# In[367]:


twitter_datadf['Tweets'][1] #Checking the format of a tweet


# In[368]:


#Cleaning column Tweets by replacing #,,,:,@user etc by ''
#Replaced each special character one by one just to keep track of changes. The code 
#twitter_datadf['Tweets'] = twitter_datadf['Tweets'].apply(lambda x: re.sub('[!@#$:).;,?&_]', '', x.lower())) combines all of these
#special characters in one and setting everything to lowercase 
twitter_datadf['Tweets'] = twitter_datadf.Tweets.str.replace('\'','') #Remove the single quote
twitter_datadf['Tweets'] = twitter_datadf.Tweets.str.replace('\,','') #Remove the comma
twitter_datadf['Tweets'] = twitter_datadf.Tweets.str.replace('\@([a-zA-Z0-9]{1,15})','') #Remove the @ mark
twitter_datadf['Tweets'] = twitter_datadf.Tweets.str.replace('\"','') #Remove the double quote
twitter_datadf['Tweets'] = twitter_datadf.Tweets.str.replace('\t','') #Remove the tab character
twitter_datadf['Tweets'] = twitter_datadf.Tweets.str.replace('RT','') #Remove the RT character
twitter_datadf['Tweets'] = twitter_datadf.Tweets.str.replace('\:','') #Remove the colon
twitter_datadf['Tweets'] = twitter_datadf.Tweets.str.replace('\#','') #Remove the hashtag
twitter_datadf['Tweets'] = twitter_datadf.Tweets.str.replace(r'http\S+','') #Remove the url
twitter_datadf['Tweets'] = twitter_datadf['Tweets'].apply(lambda x: re.sub('[!@#$:).;,?&_]', '', x.lower())) #Removing all addiitonal special characters
#twitter_datadf['Tweets'] = twitter_datadf.Tweets.str.lower() #Setting all words to lowercase
#twitter_datadf['Tweets'] = twitter_datadf['Tweets'].apply(lambda x: re.sub(u'('
#    u'\ud83c[\udf00-\udfff]|'
#    u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
#  u'[\u2600-\u26FF\u2700-\u27BF])+', '') #Had errors with these codes - the aim was was remove emoticons
twitter_datadf['Tweets'] = twitter_datadf.Tweets.str.replace(u'['u'\U0001F300-\U0001F64F,'u'\U0001F680-\U0001F6FF]','')


# In[370]:


print(twitter_datadf['Tweets'][0:40])


# In[371]:


#Splitting each tweet as a string into words
twitter_datadf['Tweets'].str.split()


# In[153]:


#Preprocessing del RT @blablabla:
twitter_datadf['tweetos'] = '' 

#add tweetos first part
for i in range(len(twitter_datadf['Tweets'])):
    try:
        twitter_datadf['Tweets'][i] = twitter_datadf['Tweets'].str.split(' ')[i][0]
    except AttributeError:    
        twitter_datadf['tweetos'][i] = 'other'

#Preprocessing tweetos. select tweetos contains 'RT @'
for i in range(len(twitter_datadf['Tweets'])):
    if twitter_datadf['Tweets'].str.contains('@')[i]  == False:
        twitter_datadf['Tweets'][i] = 'other'
        
# remove URLs, RTs, and twitter handles
for i in range(len(twitter_datadf['Tweets'])):
    twitter_datadf['Tweets'][i] = " ".join([word for word in twitter_datadf['Tweets'][i].split()
                                if 'http' not in word and '@' not in word and '<' not in word])


twitter_datadf['Tweets'][1]


# In[197]:


import re
import nltk
from nltk.corpus import stopwords
# column you are working on

print(df_[0:10])

stopword_set = set(stopwords.words("english"))

# convert to lower case and split 
df_ = df_.str.lower().split()

# remove stopwords
df_ = df_.apply(lambda x: [item for item in x if item not in stopword_set])

# keep only words
regex_pat = re.compile(r'[^a-zA-Z\s]', flags=re.IGNORECASE)
df_ = df_.str.replace(regex_pat, '')

# join the cleaned words in a list
df_.str.join("")
print(df_[0:10])


# In[ ]:


results = []
#Get the first 500 items based on the search query
for tweet in tweepy.Cursor(twitter_setup().search, q='%bringfamiliestogether').items(500):
    results.append(tweet)
print (len(results))

