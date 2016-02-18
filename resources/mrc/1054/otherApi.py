from TwitterAPI import TwitterAPI


SEARCH_TERM = 'outofservice+result'


CONSUMER_KEY = 'ZzFtWltlHls6gp3LB1KlwcB2G'
CONSUMER_SECRET = 'wpvS4AdQpgCF78RXgAtLmDaNHnqajnMS9UqDzZCrzIK6wTopPP'
ACCESS_TOKEN_KEY = '4915706369-LLbl408WVQA5k1yad9v4apOZemGgIQfJUPCTbir'
ACCESS_TOKEN_SECRET = 'yeuiH2cyDlPFzO5Ir83WzhyCuka9JlDIVMhIN9bIYMJpM'


api = TwitterAPI(CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN_KEY,
        ACCESS_TOKEN_SECRET)

r = api.request('search/tweets', {'q': SEARCH_TERM})

for item in r:
    print(item['text'] if 'text' in item else item)
