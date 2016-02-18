import twitter

def enf_type(field, _type, val):
    """ Checks to see if a given val for a field (i.e., the name of the field)
    is of the proper _type. If it is not, raises a TwitterError with a brief
    explanation.
    Args:
        field:
            Name of the field you are checking.
        _type:
            Type that the value should be returned as.
        val:
            Value to convert to _type.
    Returns:
        val converted to type _type.
    """
    try:
        return _type(val)
    except ValueError:
        raise TwitterError({
            'message': '"{0}" must be type {1}'.format(field, _type.__name__)
        })

def newGetSearch(self,
              term=None,
              raw_query=None,
              geocode=None,
              since_id=None,
              max_id=None,
              until=None,
              since=None,
              count=15,
              lang=None,
              locale=None,
              result_type="mixed",
              include_entities=None):
    """Return twitter search results for a given term. You must specify one
    of term, geocode, or raw_query.

    Args:
      term (str, optional):
        Term to search by. Optional if you include geocode.
      raw_query (str, optional):
        A raw query as a string. This should be everything after the "?" in
        the URL (i.e., the query parameters). You are responsible for all
        type checking and ensuring that the query string is properly
        formatted, as it will only be URL-encoded before be passed directly
        to Twitter with no other checks performed. For advanced usage only.
      since_id (int, optional):
        Returns results with an ID greater than (that is, more recent
        than) the specified ID. There are limits to the number of
        Tweets which can be accessed through the API. If the limit of
        Tweets has occurred since the since_id, the since_id will be
        forced to the oldest ID available.
      max_id (int, optional):
        Returns only statuses with an ID less than (that is, older
        than) or equal to the specified ID.
      until (str, optional):
        Returns tweets generated before the given date. Date should be
        formatted as YYYY-MM-DD.
      since (str, optional):
        Returns tweets generated since the given date. Date should be
        formatted as YYYY-MM-DD.
      geocode (str or list or tuple, optional):
        Geolocation within which to search for tweets. Can be either a
        string in the form of "latitude,longitude,radius" where latitude
        and longitude are floats and radius is a string such as "1mi" or
        "1km" ("mi" or "km" are the only units allowed). For example:
          >>> api.GetSearch(geocode="37.781157,-122.398720,1mi").
        Otherwise, you can pass a list of either floats or strings for
        lat/long and a string for radius:
          >>> api.GetSearch(geocode=[37.781157, -122.398720, "1mi"])
          >>> # or:
          >>> api.GetSearch(geocode=(37.781157, -122.398720, "1mi"))
          >>> # or:
          >>> api.GetSearch(geocode=("37.781157", "-122.398720", "1mi"))
      count (int, optional):
        Number of results to return.  Default is 15 and maxmimum that
        Twitter returns is 100 irrespective of what you type in.
      lang (str, optional):
        Language for results as ISO 639-1 code.  Default is None
        (all languages).
      locale (str, optional):
        Language of the search query. Currently only 'ja' is effective.
        This is intended for language-specific consumers and the default
        should work in the majority of cases.
      result_type (str, optional):
        Type of result which should be returned. Default is "mixed".
        Valid options are "mixed, "recent", and "popular".
      include_entities (bool, optional):
        If True, each tweet will include a node called "entities".
        This node offers a variety of metadata about the tweet in a
        discrete structure, including: user_mentions, urls, and
        hashtags.

    Returns:
      list: A sequence of twitter.Status instances, one for each message
      containing the term, within the bounds of the geocoded area, or
      given by the raw_query.
    """

    url = '%s/search/tweets.json' % self.base_url
    parameters = {}

    if since_id:
        parameters['since_id'] = enf_type('since_id', int, since_id)

    if max_id:
        parameters['max_id'] = enf_type('max_id', int, max_id)

    if until:
        parameters['until'] = enf_type('until', str, until)

    if since:
        parameters['since'] = enf_type('since', str, since)

    if lang:
        parameters['lang'] = enf_type('lang', str, lang)

    if locale:
        parameters['locale'] = enf_type('locale', str, locale)

    if term is None and geocode is None and raw_query is None:
        return []

    if term is not None:
        parameters['q'] = term

    if geocode is not None:
        if isinstance(geocode, list) or isinstance(geocode, tuple):
            parameters['geocode'] = ','.join([str(geo) for geo in geocode])
        else:
            parameters['geocode'] = enf_type('geocode', str, geocode)

    if include_entities:
        parameters['include_entities'] = enf_type('include_entities',
                                                  bool,
                                                  include_entities)

    parameters['count'] = enf_type('count', int, count)

    if result_type in ["mixed", "popular", "recent"]:
        parameters['result_type'] = result_type

    if raw_query is not None:
        url = "{url}?{raw_query}".format(
            url=url,
            raw_query=raw_query)
        resp = self._RequestUrl(url, 'GET')
    else:
        resp = self._RequestUrl(url, 'GET', data=parameters)

    data = self._ParseAndCheckTwitter(resp.content.decode('utf-8'))

    return [twitter.Status.NewFromJsonDict(x) for x in data.get('statuses', '')]

twitter.Api.GetSearch = newGetSearch

api = twitter.Api(consumer_key='ZzFtWltlHls6gp3LB1KlwcB2G',
        consumer_secret='wpvS4AdQpgCF78RXgAtLmDaNHnqajnMS9UqDzZCrzIK6wTopPP',
        access_token_key='4915706369-LLbl408WVQA5k1yad9v4apOZemGgIQfJUPCTbir',
        access_token_secret='yeuiH2cyDlPFzO5Ir83WzhyCuka9JlDIVMhIN9bIYMJpM')

for tweet in api.GetSearch(raw_query='q=outofservice+bigfive+results&count=50&result_type=popular', count=50):
    print tweet
