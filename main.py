import tweepy
import twitter_config

from creeper_pp.information_extractor import InformationExtractor

auth = tweepy.OAuthHandler(twitter_config.consumer_key, twitter_config.consumer_secret)
auth.set_access_token(twitter_config.access_token, twitter_config.access_token_secret)

api = tweepy.API(auth)

ie = InformationExtractor(api)
user = ie.extract('dakatapetrov', 200)
print user.hashtags_count
