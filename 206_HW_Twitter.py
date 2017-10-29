import unittest
import tweepy
import requests
import json
import twitter_info
## SI 206 - HW
## COMMENT WITH: Michele Gee
## Your section day/time: 8:30 AM MLB Basement
## Any names of people you worked with on this assignment: Aaron Kyle Priscilla


## Write code that uses the tweepy library to search for tweets with three different phrases of the
## user's choice (should use the Python input function), and prints out the Tweet text and the
## created_at value (note that this will be in GMT time) of the first FIVE tweets with at least
## 1 blank line in between each of them, e.g.


## You should cache all of the data from this exercise in a file, and submit the cache file
## along with your assignment.

## So, for example, if you submit your assignment files, and you have already searched for tweets
## about "rock climbing", when we run your code, the code should use CACHED data, and should not
## need to make any new request to the Twitter API.  But if, for instance, you have never
## searched for "bicycles" before you submitted your final files, then if we enter "bicycles"
## when we run your code, it _should_ make a request to the Twitter API.

## Because it is dependent on user input, there are no unit tests for this -- we will
## run your assignments in a batch to grade them!

## We've provided some starter code below, like what is in the class tweepy examples.

##SAMPLE OUTPUT
## See: https://docs.google.com/a/umich.edu/document/d/1o8CWsdO2aRT7iUz9okiCHCVgU5x_FyZkabu2l9qwkf8/edit?usp=sharing



## **** For extra credit, create another file called twitter_info.py that
## contains your consumer_key, consumer_secret, access_token, and access_token_secret,
## import that file here.  Do NOT add and commit that file to a public GitHub repository.

## **** If you choose not to do that, we strongly advise using authentication information
## for an 'extra' Twitter account you make just for this class, and not your personal
## account, because it's not ideal to share your authentication information for a real
## account that you use frequently.

## Get your secret values to authenticate to Twitter. You may replace each of these
## with variables rather than filling in the empty strings if you choose to do the secure way
## for EC points

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

## Set up your authentication to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Set up library to grab stuff from twitter with your authentication, and
# return it in a JSON-formatted way

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

## Write the rest of your code here!

#### Recommended order of tasks: ####
## 1. Set up the caching pattern start -- the dictionary and the try/except
## 		statement shown in class.
CACHE_FNAME = 'tweepy_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()  #read data
    CACHE_DICTION = json.loads(cache_contents) #put to dictionary
    cache_file.close()
except:
    CACHE_DICTION = {} #make a dictionary anyway



## 2. Write a function to get twitter data that works with the caching pattern,
## 		so it either gets new data or caches data, depending upon what the input
##		to search for is.
def getTweetsWithCaching(twt):
    tweet_key = 'twitter_{}'.format(twt)
    if tweet_key in CACHE_DICTION: #if statement to use cache
        print('using cache')
        return CACHE_DICTION[tweet_key]
    else:
        print('fetching') #using .search method, write to CACHE_FNAME
        public_tweets = api.search(q=twt)

        CACHE_DICTION[tweet_key] = public_tweets #####
        dumped_cache = json.dumps(CACHE_DICTION) #make JSON format
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_cache)
        fw.close
        return public_tweets



## 3. Using a loop, invoke your function, save the return value in a variable, and explore the
##		data you got back!

for i in range(3):
    twt = input('Enter Tweet term: ')
    data = getTweetsWithCaching(twt)
    twt_info = data['statuses'] #'statuses' key to enter actual tweet info
    #print(twt_info)


## 4. With what you learn from the data -- e.g. how exactly to find the
##		text of each tweet in the big nested structure -- write code to print out
## 		content from 5 tweets, as shown in the linked example.
for atweet in twt_info[:5]: #index for only 5
    print ('TEXT:',atweet['text'])
    print ('CREATED AT:',atweet['created_at'])
    print ('\n')
