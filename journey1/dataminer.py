"""
Created on 18 Jul 2016 at 21:17
@author ckan
"""
import os
import json
from datetime import datetime
import pandas as pd # pandas for data analysis/manipulation
import matplotlib.pyplot as plt # matplotlib for data visualization


class TweetExtractor:

	"""
		Extract all value related to a key
	"""
	def extract(self, key, tweets):
		data = []
		for tweet in tweets:
			self.depth_search(lookup=key, tweet=tweet, data=data)
		return data

	def depth_search(self, lookup, tweet, data):
		if isinstance(tweet, dict):
			for key in tweet.keys():
				value = tweet[key]

				if value == None:
					data.append(None)
				else:
					if lookup == key:
						if isinstance(value, unicode) or isinstance(value, str):
							data.append(value)
							#break
						elif isinstance(value, dict): # k = dict
							print value
					else:
						self.depth_search(lookup, value, data)

					#else:	
						# k = list
						#print 'do nothing'

	def first_level_extraction(self, key, tweets):
		""" Extraction de niveau 1
			Retourne sous forme de liste les valeurs des cles de niveau 1
		"""
		data = []
		for tweet in tweets:
			self.__first_level_extraction(lookup=key, tweet=tweet, data=data)
		return data

	def __first_level_extraction(self, lookup, tweet, data):
		if isinstance(tweet, dict):
			for key in tweet.keys():
				if lookup == key and isinstance(key, unicode):
					data.append(tweet[key])
					break

	def second_level_extraction(self, first_level_key, key, tweets):
		""" Extraction de niveau 2
			Retourne sous forme de liste les valeurs des cles de niveau 2
		"""
		data = []
		for tweet in tweets:
			self.__second_level_extraction(lookup=key, first_level_key=first_level_key, tweet=tweet, data=data)
		return data

	def __second_level_extraction(self, first_level_key, lookup, tweet, data):
		if isinstance(tweet, dict):
			for key in tweet.keys():
				if first_level_key == key:
					value = tweet[key]
					if value == None:
						data.append(None)
					else:
						if isinstance(value, unicode):
							data.append(value)
						elif isinstance(value, dict):
							self.__second_level_extraction(lookup, None, value, data)


""" Taille du fichier au moment de l'analyse: 103, 807 Ko """
filename = os.path.join(os.getcwd(), 'data', 'twitter_data_sample.json')
data = open(filename, 'r')

start = datetime.now()
tweets_data = [json.loads(tweet) for tweet in data]
print 'Tweets total : ', len(tweets_data)


"""for key, val in tweets_data[0].items():
	print key, val"""

"""texts = [tweet[key] for tweet in tweets_data for key in tweet.keys() if key == 'text']
langs = [tweet[key] for tweet in tweets_data for key in tweet.keys() if key == 'lang']
countries = []
for tweet in tweets_data :
	for key in tweet.keys():
		if key == 'place':
			place = tweet[key]
			if place != None:
				for cle in place.keys():
					if cle == 'country':
						countries.append(place[cle])
			else:
				countries.append(None)
print len(countries)
tweetExtractor = TweetExtractor()
texts2 = tweetExtractor.first_level_extraction(key=u'text', tweets=tweets_data)
langs2 = tweetExtractor.first_level_extraction(key=u'lang', tweets=tweets_data)
country2 = tweetExtractor.second_level_extraction(first_level_key='place', key=u'country', tweets=tweets_data)
print 'texts : ', len(texts)
print 'texts2 : ', len(texts2)
print 'langs : ', len(langs)
print 'langs2 : ', len(langs2)
print len(country2)"""

tweetExtractor = TweetExtractor()

tweets_df = pd.DataFrame() # Empty tweets DataFrame

# fill the dataFrame with values
tweets_df['text'] = tweetExtractor.first_level_extraction(key=u'text', tweets=tweets_data)
tweets_df['lang'] = tweetExtractor.first_level_extraction(key=u'lang', tweets=tweets_data)
tweets_df['country'] = tweetExtractor.second_level_extraction(first_level_key='place', key=u'country', tweets=tweets_data)

print tweets_df.head()




end = datetime.now()

print 'elapsed time : ', str(end - start)