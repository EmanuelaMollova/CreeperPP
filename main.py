import os
import twitter_config
import sys

from tweepy.error import TweepError

from creeper_pp.core import Core

credentials = {
        'consumer_key': twitter_config.consumer_key,
        'consumer_secret': twitter_config.consumer_secret,
        'access_token': twitter_config.access_token,
        'access_token_secret': twitter_config.access_token_secret
        }

core = Core(2,1, 200)
core.init_twitter(credentials)


bigfive_data = os.getcwd() + '/resources/bigfive_data.json'
sys.stdout.write('reading json... ')
sys.stdout.flush()
core.load_json(bigfive_data)
print 'done.'
print

sys.stdout.write('extracting information for users... ')
core.load_users()
print 'done.'
print

sys.stdout.write('training... ')
sys.stdout.flush()
core.train()
print 'done.'
print

def predict(uname):
    predicted = core.predict(uname)
    ocean = predicted['ocean']
    print 'Openness to Experience/Intellect: ' + str(ocean['o'])
    print 'High scorers tend to be original, creative, curious, complex; Low scorers tend to be conventional, down to earth, narrow interests, uncreative.'
    print
    print 'Conscientiousness: ' + str(ocean['c'])
    print 'High scorers tend to be reliable, well-organized, self-disciplined, careful; Low scorers tend to be disorganized, undependable, negligent.'
    print
    print 'Extraversion: ' + str(ocean['e'])
    print 'High scorers tend to be sociable, friendly, fun loving, talkative; Low scorers tend to be introverted, reserved, inhibited, quiet.'
    print
    print 'Agreeableness: ' + str(ocean['a'])
    print 'High scorers tend to be good natured, sympathetic, forgiving, courteous; Low scorers tend to be critical, rude, harsh, callous.'
    print
    print 'Neuroticism: ' + str(ocean['n'])
    print 'High scorers tend to be nervous, high-strung, insecure, worrying; Low scorers tend to be calm, relaxed, secure, hardy.'


    words = predicted['top_words']
    print 'Most used words:'
    print
    for (w, count)  in words:
        print(w)

    print

    hashtags = predicted['hashtags']
    print 'Most used hashtags:'
    print
    for (w, count)  in hashtags:
        print(w)

    print

    bigrams = predicted['bigrams']
    print 'Most used bigrams:'
    print
    for ((f, s), count)  in bigrams:
        print(f + " " + s)

    print

while True:
    print
    print '-------------------------------------------------------------------------'
    print
    input = raw_input('Enter username: ').rstrip('\n')
    print
    try:
        predict(input)
    except TweepError:
        print 'Something went wrong, please try again later.'
