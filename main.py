import tweepy
import twitter_config

from creeper_pp.information_extractor import InformationExtractor
from creeper_pp.features_extractor import FeaturesExtractor
from creeper_pp.preprocessor import Preprocessor

auth = tweepy.OAuthHandler(twitter_config.consumer_key, twitter_config.consumer_secret)
auth.set_access_token(twitter_config.access_token, twitter_config.access_token_secret)

api = tweepy.API(auth)

ie = InformationExtractor(api)
user = ie.extract('dakatapetrov', 200)
print user.id
print user.followers_count
print user.following_count
print user.total_tweets
print user.mentions_count
print user.replies_count

fe = FeaturesExtractor(user)
print fe.get_features()

# print user.tweets_text

# preprocessor = Preprocessor(user.tweets_text)

# print "\nTokens\n"
# tokens = preprocessor.tokenize()
# print tokens

# stem = preprocessor.stem()
# print "\nStem\n"
# print stem

# # lemmatize = preprocessor.lemmatize()
# # print "\nLemmatize\n"
# # print lemmatize

# pos = preprocessor.pos()
# print "\nPOS tagger\n"
# print pos

# no_stop = preprocessor.remove_stop_words_and_urls()
# print "\nNo stop words\n"
# print no_stop

# vader = preprocessor.vader()
# print "\nVader\n"
# print vader
