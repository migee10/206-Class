import datetime
import unittest
import itertools
import collections
import requests
import urllib.request
import json
import sqlite3


fb_access_token = 'EAACEdEose0cBAAZBjblUZBxgHERbhZBsyjQX4DgMDShol14GCtAdZABaepmbfccBjZAxZC7gFoe6qYedhizXXpkWmTPb1L1KQZAOpTwyXZB9snc2FXsPjKv8PVjZCt6ta3LrDuSMjqqyoWB75QMBlBJxwSx31WqzfheZBXa6aLFm0TenwuZA0W96x8eCJtLl1la8wnJsamLraZBLMwZDZD'

CACHE_FB = "facebokokcache.json"

try:
	cache_file_fb = open(CACHE_FB, 'r')
	cache_contents_fb = cache_file_fb.read()
	CACHE_DICTION_fb = json.loads(cache_contents_fb)
	cache_file_fb.close()
except:
	CACHE_DICTION_fb = {}


def fbcache(user):
	if user in CACHE_DICTION_fb:
		print('using cache facebook')
		data_fb = CACHE_DICTION_fb[user]
	else:
		print('fetching facebook')
		fb_url = 'https://graph.facebook.com/v2.11/' + user + '?fields=name,feed.limit(100)&access_token=' + fb_access_token

		req = urllib.request.urlopen(fb_url)
		read = req.read()
		data_fb = json.loads(read)
		CACHE_DICTION_fb[user] = data_fb

		dumped_json_cache = json.dumps(CACHE_DICTION_fb)
		fw = open(CACHE_FB,"w")
		fw.write(dumped_json_cache)
		fw.close()
	return data_fb

conn = sqlite3.connect('facebookok.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Facebook_Posts')
cur.execute('''CREATE TABLE Facebook_Posts (post_id TEXT PRIMARY KEY, post TEXT, created_time DATETIME)''')

fb = fbcache('me')

for f in fb['feed']['data']:
	ids = f['id']
	if 'message' in f:
		posts = f['message']
	else:
		posts = f['story']
	times = f['created_time']
	cur.execute('''INSERT INTO Facebook_Posts (post_id, post, created_time) VALUES (?, ?, ?)''', (ids, posts, times))


conn.commit()
