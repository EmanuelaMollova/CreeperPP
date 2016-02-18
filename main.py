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
from creeper_pp.personality_predictor import PersonalityPredictor

auth = tweepy.OAuthHandler(twitter_config.consumer_key, twitter_config.consumer_secret)
auth.set_access_token(twitter_config.access_token, twitter_config.access_token_secret)

api = tweepy.API(auth)
ie = InformationExtractor(api)

bigfive_data = os.getcwd() + '/resources/bigfive_data.json'
with open(bigfive_data) as data_file:
    data = json.load(data_file)

for username in data:
    user = ie.extract(username, 200)
    fe = FeaturesExtractor(user)
    data[username]['f'] = fe.get_features()

    print(username)
    print(data[username])
