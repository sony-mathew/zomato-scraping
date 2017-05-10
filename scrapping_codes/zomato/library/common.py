import socket, urllib2, hashlib, random, requests
from bs4 import BeautifulSoup
from database import *
import urlparse, urllib
import sys

class CommonBasics:
	
	def scrape(self, link):
		link = link.decode("unicode_escape")
		scheme, netloc, path, query, fragment = urlparse.urlsplit(link)
		path = urllib.quote(path.encode("utf-8"))
		link = urlparse.urlunsplit((scheme, netloc, path, query, fragment))
		# socket.setdefaulttimeout(12)
		# req = urllib2.Request(link, headers = { 'User-Agent' : self.user_agent() })
		try:
			# self.response = urllib2.urlopen(req).read()
			self.response = requests.get(link, timeout = 12, headers = self.headers())
			self.content = self.response.content
		except HTTPError as e:
			sys.stdout.write('The server couldn\'t fulfill the request. Link : ' + link)
			self.response = False
		except URLError as e:
			sys.stdout.write('We failed to reach a server. Link : ' + link)
			self.response = False

		if self.content :
			self.soup = BeautifulSoup(self.content, 'html.parser')
			
	def sterilize(self, txt, custom_chars = []):
		replace = ["\n", "\r", "\t"]
		replace.extend(custom_chars)
		txt = txt.replace("  ", " ")
		for item in replace:
			txt = txt.replace(item, "")
		return txt.encode('unicode_escape')

	def toUnicode(self, text):
		return ''.join([i if ord(i) < 128 else ' ' for i in text])

	def get_hash(self, text):
		return hashlib.md5(self.toUnicode(text)).hexdigest()

	def insert_source(self, link, hash_md5):
		new_source = Source.create(link=link, hash_md5=hash_md5)
		return new_source.id

	def user_agent(self):
		agents = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
		"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13; ) Gecko/20101203"]
		return random.choice(agents)

	def headers(self):
		return {
			'User-Agent' : self.user_agent(),
			'Accept-Language' : 'en-gb'
		}

	def toNum(self, val):
		try:
			val = self.sterilize(val)
			return filter(lambda x: x.isdigit() or x =='.', val)
		except:
			return '0'

	def toInt(self, val):
		try:
			return int(self.toNum(val))
		except:
			return 0

	def toFloat(self, val):
		try:
			return float(self.toNum(val))
		except:
			return 0.0
