class FeaturesConverter(object):
    vector_features_cnt = 28
    features = [
            "followers_cnt",
            "following_cnt",
            "total_tweets",
            "mentions_cnt",
            "replies_cnt",
            "hashtags_cnt",
            "links_cnt",
            "words_cnt",
            "tweets_cnt",
            "tokens_len",

            "neg",
            "pos",
            "neu",
            "compaund",

            "nlet",
            "nphon",
            "nsyl",
            "kffreq",
            "kfncats",
            "kfnsamp",
            "tl",
            "brownf",
            "fam",
            "conc",
            "imag",
            "meanp",
            "meanc",
            "aoa",

            "id",
            "tweets",
            "top_words",
            "hashtags",
            "bigrams",

            "o_metric",
            "c_metric",
            "e_metric",
            "a_metric",
            "n_metric"
            ]
    last_int_index = features.index('tokens_len')
    last_float_index = features.index('aoa')

    @classmethod
    def make_float(self, value):
        if isinstance(value, basestring):
            return float(re.sub("[^0-9.]", "", value))
        else:
            return float(value)


    @classmethod
    def convert_features_to_solr(self, all_features_dict):
        solr_features_vec = []
        for user_id in all_features_dict:
            features_dict = all_features_dict[user_id]
            solr_features = {}
            solr_features['id'] = user_id
            solr_features['tweets'] = features_dict['tweets']
            solr_features['top_words'] = features_dict['top_words']
            solr_features['tweets'] = features_dict['hashtags']
            solr_features['tweets'] = features_dict['bigrams']
            solr_features['o_metric'] = self.make_float(features_dict['o'])
            solr_features['c_metric'] = self.make_float(features_dict['c'])
            solr_features['e_metric'] = self.make_float(features_dict['e'])
            solr_features['a_metric'] = self.make_float(features_dict['a'])
            solr_features['n_metric'] = self.make_float(features_dict['n'])
            features = features_dict['f']
            for i in range(len(features)):
                solr_features[self.features[i]] = features[i]
            solr_features_vec.append(solr_features)
        return solr_features_vec


    @classmethod
    def convert_solr_to_features(self, solr_features):
        user_dict = {}
        features_dict = {}
        print solr_features
        features_dict['tweets'] = solr_features['tweets']
        features_dict['top_words'] = solr_features['top_words']
        features_dict['hashtags'] = solr_features['hashtags']
        features_dict['bigrams'] = solr_features['bigrams']
        features_dict['o'] = solr_features['o_metric']
        features_dict['c'] = solr_features['c_metric']
        features_dict['e'] = solr_features['e_metric']
        features_dict['a'] = solr_features['a_metric']
        features_dict['n'] = solr_features['n_metric']
        vector = [0 for x in range(self.vector_features_cnt)]
        for key in solr_features:
            index = self.features.index(key)
            if index <= self.last_int_index:
                vector[index] = int(solr_features[key])
            elif index <= self.last_float_index:
                vector[index] = float(solr_features[key])
        features_dict['f'] = vector
        user_dict[solr_features['id']] = features_dict
        return user_dict
