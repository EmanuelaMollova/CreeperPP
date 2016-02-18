import os
import json
import tweepy
import twitter_config

from creeper_pp.information_extractor import InformationExtractor
from creeper_pp.features_extractor import FeaturesExtractor
from creeper_pp.preprocessor import Preprocessor
from creeper_pp.io_service import IoService
from creeper_pp.shell_service import ShellService
from creeper_pp.mrc_service import MrcService
# from creeper_pp.personality_predictor import PersonalityPredictor

from tweepy.error import TweepError

auth = tweepy.OAuthHandler(twitter_config.consumer_key, twitter_config.consumer_secret)
auth.set_access_token(twitter_config.access_token, twitter_config.access_token_secret)

api = tweepy.API(auth)
ie = InformationExtractor(api)

user = ie.extract('Sriracha_Queen', 200)
preprocessor = Preprocessor(user.tweets_text)
preprocessor.most_used_words()
preprocessor.most_used_hashtags()
preprocessor.most_used_bigrams()

bigfive_data = os.getcwd() + '/resources/bigfive_data.json'
print 'reading json...'
with open(bigfive_data) as data_file:
    data = json.load(data_file)

to_remove = []

cnt = 100
i = 0

for username in data:
    print 'extracting information for user ' + username + '...'
    try:
        user = ie.extract(username, 200)
        fe = FeaturesExtractor(user)
        data[username]['f'] = fe.get_features()
        i += 1
        if i == cnt:
            break
    except ZeroDivisionError:
        print 'meh ' + username
        if username in data:
            to_remove.append(username)
    except TweepError:
        print 'capacity'
        if username in data:
            to_remove.append(username)

for uname in to_remove:
    if uname in data:
        del data[uname]

pp = PersonalityPredictor()
print 'registering data...'
pp.register(data)
print 'training...'
pp.train()

print 'predicting'
user_ = ie.extract('skanev', 200)
user_fe = FeaturesExtractor(user_)
user_features = user_fe.get_features()
print pp.predict(user_features)
