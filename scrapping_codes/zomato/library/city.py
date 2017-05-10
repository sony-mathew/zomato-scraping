from common import *
from database import * 
from links import * 
from IPython import embed


class ScrapeCityBasePage(CommonBasics):

	def __init__(self, city, link):
		self.city = city
		#for first page scraping
		# self.scrape(city.link)
		#for rest of the pages
		self.scrape(link)

		self.parseContent()

	def parseContent(self):
		# self.set_city_pages()  #for first page
		listings = self.soup.select('.search-result')
		for item in listings:
			self.save_listing_link(item)
		self.set_crawled_flag()
		sys.stdout.write("(" + str(len(listings)) + "), ")

	def save_listing_link(self, item):
		link = self.sterilize(item.select('.result-title')[0].get('href'), [" "])
		res_name = self.sterilize(item.select('.result-title')[0].getText())
		address = self.sterilize(item.select('.search-result-address')[0].get('title'))
		cuisine = self.sterilize(item.select('.res-snippet-small-cuisine')[0].get('title'))
		price_range = len(item.select('.cft_symbols .cft_bold'))
		rate = item.select('.res-rating-nf')
		if len(rate) > 0 :
			rating = self.sterilize(rate[0].getText(), [" "])
		else:
			rating = 0
		votes = item.select('.rating-rank')
		if len(votes) > 0:
			voted_users = self.sterilize(votes[0].getText(), [" "])
		else:
			voted_users = 0
		

		Listing.create(city = self.city.id, 
										name = res_name, 
										address = address, 
										cuisine = cuisine, 
										price_range = price_range,
										rating = rating,
										voted_users = voted_users,
										link = link)
		
	def set_city_pages(self):
		try:
			pages = self.soup.select('.pagination-number')[0].get('aria-label').split('of')[1]
			pages = int(pages)
		except:
			pages = 0

		self.city.pages = pages
		self.city.save()

	def set_crawled_flag(self):
		# self.city.crawled = True #for first page scraping
		self.city.pages_crawled += 1
		if self.city.pages_crawled == self.city.pages :
			self.city.finished = True
		self.city.save()
			