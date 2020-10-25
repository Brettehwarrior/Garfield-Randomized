import tweepy

# Get API keys from keys.txt in root
# keys.txt is hidden in repository for obvious reasons
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

TWEET_COUNTER_FILE = 'tweet_counter.txt'

def read_counter() -> int:
    """Returns current value in tweet_counter.txt"""
    data = -1
    with open(TWEET_COUNTER_FILE, 'r') as f:
        data = f.read()
        f.close()
    return int(data)


def increment_counter(count: int):
    """Increases the tweets counter in tweet_counter.txt"""
    count += 1
    with open(TWEET_COUNTER_FILE, 'w') as f:
        f.write(str(count))
        f.close()


def send_tweet(template_text: str, credit_text: str) -> str:
    """Sends a tweet with the current output image attatched containing comic number and template info"""
    
    count = read_counter()
    
    # Send random garf
    tweet = api.update_with_media('images/tweet.png', f'Randomized Garfield comic #{count} {template_text}')
    
    increment_counter(count)
    
    #Reply with sources
    reply = api.update_status(credit_text, tweet.id)
    
    return f"Tweet: {tweet.id}\nReply: {reply.id}"


    