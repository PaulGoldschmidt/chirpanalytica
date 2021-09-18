# Downloadscript for chirpanalytica (ca)
import tweepy
import time
import csv
import sys
import json
import re  # re: für die wegkürzung der URLs aus den Tweets
from datetime import datetime
from datetime import timedelta
sys.path.append('../')
from cleanuptext import clean_text

print("Starting downloading tweets. Standby...")

now = datetime.now()
print("Starttime:")
print(now.strftime("%Y-%m-%d %H:%M:%S"))
starttime = time.perf_counter()

# Counter für Statistiken
count_success = 0
count_fail = 0
count_tweets = 0

#Import twitter credentials from file
with open('../twittercredentials.json') as data_file:
    data = json.load(data_file)

consumer_key = data['consumerKey']
consumer_secret = data['consumerSecret']
access_key = data['accessTokenKey']
access_secret = data['accessTokenSecret']

# Outputdatei
outfile = "data/tweets.csv"

with open('data/usernames.csv', 'rt') as f:
    # Skip header line
    next(f)

    print("Read CSV with users.")

    rows = list(csv.reader(f))
    party_mapping = {}
    for _, _, username, _, party in rows:
        if party in party_mapping:
            party_mapping[party].append(username)
        else:
            party_mapping[party] = [username]

    for party, usernames in party_mapping.items():
        # Ignore parties with less than 10 twitter usernames
        if len(usernames) < 10:
            continue

        for username in usernames:
            # Twitter Auth
            # http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_key, access_secret)
            api = tweepy.API(auth, wait_on_rate_limit=True,
                             wait_on_rate_limit_notify=True)
            try:
                u = api.get_user(username)
                print("Downloading tweets from " + username + " with the User-ID " + u.id_str +
                      " from the party " + party + " and the display name " + u.screen_name + ".")

                # so viele Tweets werden maximal heruntergeladen
                number_of_tweets = 250

                # Aktuelles Datum mit timedelta subtrahieren, dann in past speichern
                past = datetime.today() - timedelta(days=60)

                # get tweets
                with open(outfile, 'a') as file:
                    writer = csv.writer(file, delimiter=',')
                    for tweet in tweepy.Cursor(api.user_timeline, screen_name=username).items(number_of_tweets):
                        # create array of tweet information: username, tweet id, date/time, text
                        tweettime = tweet.created_at
                        status = api.get_status(tweet.id_str, tweet_mode="extended")
                        # check, ob kriterien für tweetspeicherung erfüllt sind.
                        if tweettime < past:
                            print("Tweets from now on to old.")
                            break
                        print(status.full_text)
                        newtweettext = status.full_text
                        newtweettext = clean_text(str(newtweettext))
                        tweetlengh = str(newtweettext).count('')
                        if tweetlengh > 4: #tweet should be longer than 4 characters
                            continue
                        writer.writerow([username, party, tweet.id_str, tweet.created_at, newtweettext])
                        count_tweets = count_tweets + 1
                        print("Downloaded tweet number " +
                                str(count_tweets) + ".")
                    count_success += 1
                    print("Done downloading account, going to the next account")
            except Exception as err:
                print(err)
                print("An error has occurred. Skipping account.")
                count_fail += 1

print("\n \nDone downloading tweets! \nValid accounts: " + str(count_success) + " | Fails: " + str(count_fail) +
      "\nTotal downloaded tweets: " + str(count_tweets) + "\nThe script took " + str(time.perf_counter() - starttime) + " seconds to execute. \nExiting script.")
