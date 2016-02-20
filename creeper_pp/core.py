import json
import tweepy
import twitter_config
import sys
import re

from tweepy.error import TweepError

from creeper_pp.information_extractor import InformationExtractor
from creeper_pp.features_extractor import FeaturesExtractor
from creeper_pp.preprocessor import Preprocessor
from creeper_pp.io_service import IoService
from creeper_pp.shell_service import ShellService
from creeper_pp.mrc_service import MrcService
from creeper_pp.personality_predictor import PersonalityPredictor
from creeper_pp.features_converter import FeaturesConverter
from creeper_pp.solr_service import SolrService

class Core(object):
    def __init__(self, train_count, knn_count, tweet_count, search_config):
        self.train_count = train_count
        self.knn_count = knn_count
        self.tweet_count = tweet_count
        self.search_config = search_config
        self.pp = PersonalityPredictor(knn_count)
        self.solr = SolrService('user')

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
            if i == self.train_count:
                break
            solr_data = self.get_solr_user(username)
            if solr_data:
                self.data[username] = solr_data[username]
                i += 1
                continue

            try:
                user = self.ie.extract(username, self.tweet_count)
                fe = FeaturesExtractor(user)
                self.data[username]['f'] = fe.get_features()
                if user.tweets_text == '':
                    continue
                self.data[username]['tweets'] = user.tweets_text
                preprocessor = Preprocessor(user.tweets_text)
                self.data[username]['top_words'] = preprocessor.most_used_words(max_count=self.search_config['top_words'])
                self.data[username]['hashtags'] = preprocessor.most_used_hashtags(max_count=self.search_config['top_hashtags'])
                self.data[username]['bigrams'] = preprocessor.most_used_bigrams(max_count=self.search_config['top_bigrams'])
                if self.data[username]['hashtags'] == '':
                    self.data[username]['hashtags'] = '$'
                if self.data[username]['bigrams'] == '':
                    self.data[username]['bigrams'] = '$'
                if self.data[username]['top_words'] == '':
                    self.data[username]['top_words'] = '$'
                solr_dict = FeaturesConverter.convert_features_to_solr({username: self.data[username]})
                self.solr.addUser(solr_dict[0])
                i += 1
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

    def get_solr_user(self, username):
        solr_user =  self.solr.getUser(username)
        if solr_user:
            return FeaturesConverter.convert_solr_to_features(solr_user)
        else:
            return None

    def split_data(self, string, delimiter = ' '):
        return string.split(delimiter)

    def split_bigrams(self, string):
        return self.split_data(string, '|')

    def predict(self, username):
        prediction_dict = {}
        solr_user =  self.get_solr_user(username)
        if solr_user:
            print 'got data'
            prediction_dict = solr_user
        else:
            user = self.ie.extract(username, self.tweet_count)
            user_fe = FeaturesExtractor(user)
            user_features = user_fe.get_features()
            predicted = self.pp.predict(user_features)
            preprocessor = Preprocessor(user.tweets_text)
            prediction_dict = {
                 username: {
                     'f': user_features,
                     'o': predicted['o'],
                     'c': predicted['c'],
                     'e': predicted['e'],
                     'a': predicted['a'],
                     'n': predicted['n'],
                     'tweets': user.tweets_text,
                     'top_words': preprocessor.most_used_words(max_count=self.search_config['top_words']),
                     'hashtags': preprocessor.most_used_hashtags(max_count=self.search_config['top_hashtags']),
                     'bigrams': preprocessor.most_used_bigrams(max_count=self.search_config['top_bigrams'])
                     }
                 }
            if prediction_dict[username]['hashtags'] == '':
                prediction_dict[username]['hashtags'] = '$'
            if prediction_dict[username]['bigrams'] == '':
                prediction_dict[username]['bigrams'] = '$'
            if prediction_dict[username]['top_words'] == '':
                prediction_dict[username]['top_words'] = '$'
            if prediction_dict[username]['tweets'] == '':
                prediction_dict[username]['tweets'] = '$'
            solr_dict = FeaturesConverter.convert_features_to_solr(prediction_dict)
            self.solr.addUser(solr_dict[0])
        similar = self.solr.getSimilarUsers(username, tf=self.search_config['tf'], df=self.search_config['df'], count=self.search_config['similar'])
        prediction_dict[username].update({
            'similar': similar,
            'top_words': self.split_data(prediction_dict[username]['top_words']),
            'hashtags': self.split_data(prediction_dict[username]['hashtags']),
            'bigrams': self.split_bigrams(prediction_dict[username]['bigrams']),
            })
        return prediction_dict
