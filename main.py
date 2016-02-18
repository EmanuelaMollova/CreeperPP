import os
import json
import tweepy
import twitter_config
import sys

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
sys.stdout.write('reading json... ')
sys.stdout.flush()
with open(bigfive_data) as data_file:
    data = json.load(data_file)
print 'done.'
print

to_remove = []

cnt = 200
i = 0

for username in data:
    sys.stdout.write('extracting information for user ' + username + '... ')
    sys.stdout.flush()
    try:
        user = ie.extract(username, 200)
        fe = FeaturesExtractor(user)
        data[username]['f'] = fe.get_features()
        i += 1
        print 'done.'
        print
        if i == cnt:
            break
    except ZeroDivisionError:
        print 'fail.'
        print
        if username in data:
            to_remove.append(username)
    except TweepError:
        print 'fail.'
        print
        if username in data:
            to_remove.append(username)

for uname in to_remove:
    if uname in data:
        del data[uname]

pp = PersonalityPredictor()
sys.stdout.write('registering data... ')
sys.stdout.flush()
pp.register(data)
print 'done. '
print
sys.stdout.write('training... ')
pp.train()
sys.stdout.flush()
print 'done.'
print

def predict(uname):
    user = ie.extract(uname, 200)
    user_fe = FeaturesExtractor(user)
    user_features = user_fe.get_features()
    predicted = pp.predict(user_features)
    print 'Openness to Experience/Intellect: ' + str(predicted[0].tolist()[0])
    print 'High scorers tend to be original, creative, curious, complex; Low scorers tend to be conventional, down to earth, narrow interests, uncreative.'
    print
    print 'Conscientiousness: ' + str(predicted[1].tolist()[0])
    print 'High scorers tend to be reliable, well-organized, self-disciplined, careful; Low scorers tend to be disorganized, undependable, negligent.'
    print
    print 'Extraversion: ' + str(predicted[2].tolist()[0])
    print 'High scorers tend to be sociable, friendly, fun loving, talkative; Low scorers tend to be introverted, reserved, inhibited, quiet.'
    print
    print 'Agreeableness: ' + str(predicted[3].tolist()[0])
    print 'High scorers tend to be good natured, sympathetic, forgiving, courteous; Low scorers tend to be critical, rude, harsh, callous.'
    print
    print 'Neuroticism: ' + str(predicted[4].tolist()[0])
    print 'High scorers tend to be nervous, high-strung, insecure, worrying; Low scorers tend to be calm, relaxed, secure, hardy.'

while True:
    print
    print '-------------------------------------------------------------------------'
    print
    input = raw_input('Enter username: ').rstrip('\n')
    print
    predict(input)
