import tweepy
import sys
import predict
import statistics
import json
from datetime import datetime
from datetime import timedelta
sys.path.append("..")
from textcleaner import cleanup
sys.path.pop()

# Import Twitter credentials from file
with open('../twittercredentials.json') as data_file:
    data = json.load(data_file)

consumer_key = data['consumerKey']
consumer_secret = data['consumerSecret']
access_key = data['accessTokenKey']
access_secret = data['accessTokenSecret']


def predict_party(twitter_handle):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    # Limit number of Tweets being downloaded to analyze
    number_of_tweets = 50
    toshort = 0
    tweetsread = 0

    # Start 60 days in the past
    past = datetime.today() - timedelta(days=60)
    predictions = {}
    tweets = []
    print("Serving request of downloading user \"" + str(twitter_handle) + "\"")
    try:
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=twitter_handle).items(number_of_tweets):
            # Create array of Tweet information: username, tweet id, date/time, text
            tweettime = tweet.created_at
            status = api.get_status(tweet.id_str, tweet_mode="extended")
            # Check whether the criteria for analyzing tweets are met
            if tweettime > past:
                newtweettext = cleanup(str(status.full_text))
                tweetlengh = str(newtweettext).count('')
                # Ensure that the Tweet is longer than 4 characters
                if tweetlengh > 4:
                    tweets.append(newtweettext)
                else:
                    toshort = toshort + 1
            else:
                break

    except:
        print("Request failed.")
        return dict({"success": False, "error": 440, "data": {}, "tweetsread": 0})

    for tweet in tweets:
        prediction = predict.predict(tweet)
        tweetsread = tweetsread + 1
        for key, value in prediction.items():
            if key not in predictions.keys():
                predictions[key] = []
            predictions[key].append(value)

    for key, value in predictions.items():
        predictions[key] = statistics.mean(value)
    print("Success. Downloaded and analyzed in total " +
          str(tweetsread) + " tweets. Exiting with return of results.")
    return dict({"success": True, "error": {}, "data": predictions, "tweetsread": tweetsread})


# Only executed when called manually
if __name__ == '__main__':
    result = predict_party(sys.argv[1])
    print(json.dumps(result))
    exit(0)