
# coding: utf-8

# In[ ]:


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


# In[ ]:


#Splitting each tweet as a string into words
twitter_datadf['Tweets'].str.split()

