# Curso BigData & Data Analytics by Handytec
# Fecha: Marzo-2016
# Descripcion: Programa que cosecha tweets de una cuenta de usuario en particular

from rauth import OAuth1Service

# Get a real consumer key & secret from https://dev.twitter.com/apps/new
twitter = OAuth1Service(
    name='twitter',
    consumer_key='ppB0z1Og0fLuY7BgyhA4CZF6D',
    consumer_secret='zVsworsXDEJruStwrLFzL0vwLMAYa1lv71hYGPveNWrgCQuoKu',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    base_url='https://api.twitter.com/1.1/')

request_token, request_token_secret = twitter.get_request_token()

authorize_url = twitter.get_authorize_url(request_token)

print 'Visit this URL in your browser: ' + authorize_url
pin = raw_input('Enter PIN from browser: ')

session = twitter.get_auth_session(request_token,
                                   request_token_secret,
                                   method='POST',
                                   data={'oauth_verifier': pin})

params = {'screen_name': 'ECU911Quito',  # User to pull Tweets from
          'include_rts': 1,         # Include retweets
          'count': 10}              # 10 tweets

r = session.get('statuses/user_timeline.json', params=params)

for i, tweet in enumerate(r.json(), 1):
    handle = tweet['user']['screen_name'].encode('utf-8')
    text = tweet['text'].encode('utf-8')
    print '{0}. @{1} - {2}'.format(i, handle, text)