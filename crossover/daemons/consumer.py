import os
import sys
import signal
import tweepy
import json
import psycopg2
import urlparse


def sigterm(signal=None, frame=None):
  print 'Consumer received SIGTERM and will exit'
  sys.exit(0)


class Stream(object):

  def __init__(self):
    consumer_key = 'jQVd0Owz6hUgZVgIBXITQ'
    consumer_secret = '7MwNUTm7UOgniYpte7coMIf3xsdTW5k2lVC32sPH0C4'
    access_token = '1897180100-Ik6t5XA3iB7zGHJiHRv2xYR7Ok9PpxP8vpIfxmv'
    access_token_secret = '63EttThTgEpR3VMV3OQzqhardcS03nXAD7ZNlx7lwX4'

    self._auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    self._auth.set_access_token(access_token, access_token_secret)

    self._terms = ['pattern', 'connection', 'material', 'limits', 'nature', 'element']

  def run(self):
    sapi = tweepy.streaming.Stream(self._auth, CustomStreamListener(Database(self._terms), Parser(self._terms)))
    sapi.filter(track=self._terms)


class CustomStreamListener(tweepy.StreamListener):

  def __init__(self, database, parser):
    self._database = database
    self._parser = parser

  def on_data(self, tweet):
    data = self._parser.parse(tweet)
    if data is not None: self._database.insert(data)

    # if data is not None:  print data, '\n'
    # if data is not None: print data['term'], '\n', data['tweet']['text'], '\n', data['tweet']['user']['screen_name'], '\n\n'

    return True

  def on_error(self, status):
    print status
    return True

  def on_timeout(self):
    print 'Timeout Error'
    return True


class Parser(object):

  def __init__(self, terms):
    self._terms = terms

  def parse(self, tweet):
    try:
      tweet = json.loads(tweet)
      for term in self._terms:
        if term in tweet['text'].lower():
          return {'term':term, 'tweet':tweet}
    except:
      print 'Parser Error'
      return None


class Database(object):

  def __init__(self, terms):
    self._terms = terms
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    self._dsn = 'dbname={0} user={1} password={2} host={3} port={4}'.format( url.path[1:], url.username, url.password, url.hostname, url.port)
    self.create()

  def create(self):
    with psycopg2.connect(self._dsn) as connection:
      with connection.cursor() as cursor:
        cursor.execute(
          """
          DROP TABLE crossover_tweet
          """
        )
        cursor.execute(
          """
          CREATE TABLE crossover_tweet
          (
            id INT PRIMARY KEY,
            term TEXT UNIQUE,
            text TEXT,
            screen_name TEXT
          )
          """
        )
        cursor.executemany(
          """
          INSERT INTO crossover_tweet (id, term, text, screen_name)
          VALUES (%s, %s, %s, %s)
          """,
          [(index, value, '', '') for index, value in enumerate(self._terms)]
        )

  def insert(self, data):
    with psycopg2.connect(self._dsn) as connection:
      with connection.cursor() as cursor:
        cursor.execute(
          """
          UPDATE crossover_tweet
          SET text=%(text)s, screen_name=%(screen_name)s
          WHERE term=%(term)s;
          """,
          {
            'term':data['term'],
            'text':data['tweet']['text'],
            'screen_name':data['tweet']['user']['screen_name']
          }
        )


if __name__ == '__main__':
  signal.signal(signal.SIGTERM, sigterm)

  stream = Stream()
  stream.run()
