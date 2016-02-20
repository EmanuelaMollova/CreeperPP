import json
import tweepy
import twitter_config
import sys

from tweepy.error import TweepError

from creeper_pp.information_extractor import InformationExtractor
from creeper_pp.features_extractor import FeaturesExtractor
from creeper_pp.preprocessor import Preprocessor
from creeper_pp.io_service import IoService
from creeper_pp.shell_service import ShellService
from creeper_pp.mrc_service import MrcService
from creeper_pp.personality_predictor import PersonalityPredictor
from creeper_pp.features_converter import FeaturesConverter
from creeper_pp.features_converter import FeaturesConverter

class Core(object):
    def __init__(self, train_count, knn_count, tweet_count):
        self.train_count = train_count
        self.knn_count = knn_count
        self.tweet_count = tweet_count
        self.pp = PersonalityPredictor(knn_count)

    def load_json(self, path):
        with open(path) as data_file:
            self.data = json.load(data_file)

    def init_twitter(self, credentials):
        self.auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
        self.auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])
        self.api = tweepy.API(self.auth)
        self.ie = InformationExtractor(self.api)

    def load_users(self):
        i = 0
        to_remove = []
        for username in self.data:
            try:
                user = self.ie.extract(username, self.tweet_count)
                fe = FeaturesExtractor(user)
                self.data[username]['f'] = fe.get_features()
                self.data[username]['tweets'] = user.tweets_text
                i += 1
                if i == self.train_count:
                    break
            except ZeroDivisionError:
                if username in self.data:
                    to_remove.append(username)
            except TweepError:
                if username in self.data:
                    to_remove.append(username)
        for uname in to_remove:
            if uname in self.data:
                del self.data[uname]

    def train(self):
        self.pp.register(self.data)
        self.pp.train()

    def predict(self, uname):
        user = self.ie.extract(uname, 200)
        user_fe = FeaturesExtractor(user)
        user_features = user_fe.get_features()
        predicted = self.pp.predict(user_features)
        preprocessor = Preprocessor(user.tweets_text)
        return {
                'ocean': predicted,
                'words': preprocessor.most_used_words(),
                'hashtags': preprocessor.most_used_hashtags(),
                'bigrams': preprocessor.most_used_bigrams()
                }
