#imports
import tweepy
import garf
from time import sleep

#Get API keys from keys.txt in root
keys = open('keys.txt', 'r')
consumer_key = keys.readline().rstrip()
consumer_secret = keys.readline().rstrip()
access_token = keys.readline().rstrip()
access_token_secret = keys.readline().rstrip()
keys.close()

#API object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Tweet loop
while True:
    #How many tweets have been
    with open('tweet_counter.txt', 'r') as f:
        data = f.read()
        count = int(data)

    #Generate random garf
    garf.generate_comic()
    #Send random garf
    tweet = api.update_with_media('comic.jpg', "Randomized Garfield comic #"+str(count))
    print("Successfully sent tweet with id "+str(tweet.id))

    #Reply with sources
    msg = ''
    for url in garf.url:
        msg += url + '\n'
    reply = api.update_status('Sources:\n'+msg, tweet.id)
    print("Successfully sent reply with id "+str(reply.id))

    #Increase amount of tweets in text file
    count += 1
    with open('tweet_counter.txt', 'w') as f:
        f.write(str(count))

    #Wait before tweeting again (900 seconds == 15 minutes, 1800 seconds == 30 minutes)
    sleep(1800)
