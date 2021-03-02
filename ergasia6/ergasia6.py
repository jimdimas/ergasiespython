import tweepy
import json
import re

consumer_key="evlrZe5Egg6FvEDVRx0E5VB9X"
consumer_secret="xk4eN3Tpl907vqkpNQG8Y7RN3kuSB6TLrBFMDAXPW4d5x7Kjx8"
access_token="1356218467511316482-BuZqQS5P473kRfWDFBtXISdk3hE8fE"
access_token_secret="wP1RxOFCKjVEhT1icFjaN8hT8zC5LyAdVBGnGnkCR08iI"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def return_tweets(username): #Gets the Twitter username and if it exists,returns a list with all the individual words from that user's last ten tweets.
    tweet_words=[]           #If the user doesn't exist,the function prints an error message and returns False.
    try:
        """
        The user_timeline method gives us the timeline of the given user,given that he exists.The first argument passed is the username.
        The second argument 'count' allows us to pick a maximum number of tweets from the user's timeline.
        The third argument 'include_rts' allows us to have or not have retweets returned.I've chosen not to include retweets.
        The last argument 'tweet_mode' is set to 'extended' in order to get the full text from the tweets.
        """
        tweets=api.user_timeline(screen_name=username,count=10,include_rts=False,tweet_mode='extended')
    except: #In case no user with the given username exists.
        print("No twitter user with the given username exists.")
        return False

    for tweet in tweets[0:]:  #Tweets is an STATUS object.We will loop through each tweet included,convert it into JSON and get the tweet text.
        json_tweet=json.dumps(tweet._json) #In lines 30 and 31 we convert the STATUS Tweepy object into JSON
        json_tweet=json.loads(json_tweet,strict=False)
        tweet_text=re.sub(r'http\S+','',json_tweet["full_text"]) #In lines 32 to 37 we split the text in words and deleting links,tags and hashtags.
        tweet_text=re.sub(r'@\S+','',tweet_text)
        tweet_text=re.sub(r'#\S+','',tweet_text)
        tweet_text=re.sub(r' \d+','',tweet_text)
        tweet_text=re.sub(r"['’]",'',tweet_text) #The characters ' and ’ are converted into '' in order to convert words such as 'it's' to 'its'.
        tweet_text=re.sub(r'[^\w\s]',' ',tweet_text) #Getting rid of commas,periods etc and converting them to ' ' in order to have every word split by a space characters.

        for word in tweet_text.split():
            if word.lower() in tweet_words: #If a word is already included,it isn't added into the returned list.
                continue
            else:
                tweet_words.append(word.lower())

    return tweet_words


#Main program

username=input("Give Twitter username (also known as the user's tag '@Someone'): ")
tweets=return_tweets(username)

if tweets!=False:  #Tweets is False when the user given doesn't exist.
    if len(tweets)>=10: #Making sure the user's last ten tweets have 10 or more words.
        max_words=[]
        min_words=[]
        for i in range(5):
            temp=max(tweets,key=len)
            max_words.append(temp)
            tweets.remove(temp)
            temp=min(tweets,key=len)
            min_words.append(temp)
            tweets.remove(temp)
        print(f"The five different largest words are: {max_words[0]},{max_words[1]},{max_words[2]},{max_words[3]},{max_words[4]}")
        print(f"The five different smallest words are: {min_words[0]},{min_words[1]},{min_words[2]},{min_words[3]},{min_words[4]}")
    else:
        print("Twitter user given has less than 10 different words in his last 10 tweets.")
