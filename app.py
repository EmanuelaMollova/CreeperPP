import os
import twitter_config
import solr_config
import sys

from tweepy.error import TweepError

from creeper_pp.core import Core

import web

credentials = {
        'consumer_key': twitter_config.consumer_key,
        'consumer_secret': twitter_config.consumer_secret,
        'access_token': twitter_config.access_token,
        'access_token_secret': twitter_config.access_token_secret
        }

core = Core(solr_config.train_count,
        solr_config.knn,
        solr_config.tweet_count,
        solr_config.search_config)
core.init_twitter(credentials)

bigfive_data = os.getcwd() + '/resources/bigfive_data.json'
core.load_json(bigfive_data)

core.load_users()

core.train()

urls = (
  '/(.*)', 'index'
)

app = web.application(urls, globals())
render = web.template.render('templates/')

class index:
    def GET(self, name):
        greeting = "Hello World"
        params = {}
        params['greeting'] = greeting

        return render.index()

    def POST(self, name):
        params = {}
        input = web.input()
        user_id = input['name']
        try:
            predicted = core.predict(user_id)
            params = predicted[user_id]
            params['error'] = False
            params['user'] = user_id
            print(params)
        except TweepError:
            params['error'] = True
        return render.post(params = params)

if __name__ == "__main__":
    app.run()
