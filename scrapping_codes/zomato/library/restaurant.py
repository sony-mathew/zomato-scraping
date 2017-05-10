from common import *
from database import * 
from links import * 
import sys

class ScrapeRestaurant(CommonBasics):

	def __init__(self):
		self.scrape(self.c_link)
		self.parseContent()

	def parseContent(self):
		self.parseHeader()
		self.order_now()
		self.leftSidebarDetails()

	def parseHeader(self):
		self.breadcrumb = self.sterilize(self.soup.select(".breadcrumb")[0].get_text())
		header = self.soup.select(".resbox__header")[0]
		self.restaurant_type = self.sterilize(header.select(".res-info-estabs")[0].get_text())
		self.name = self.sterilize(header.select(".res-name")[0].get_text())
		self.rating = self.toFloat(header.select(".rating-div")[0].get_text())
		self.votes = self.toInt(header.select(".rating-div")[0].get_text())
		self.bg_image_url = self.soup.select("#progressive_image")[0]['data-url']

	def order_now(self):
		order_now = self.soup.select(".order-now-banner")
		self.order_now = len(order_now)
		if self.order_now > 0 :
			self.min_order = self.toInt(self.toNum(order_now.select(".min-order-section")[0].get_text()).strip('.'))
			self.delivery_rating = 5 - len(order_now.select(".unstar"))
			self.delivery_time = self.toInt(order_now.select(".del-time-section .cblack")[0].get_text())

	def leftSidebarDetails(self):
		sidebar = self.soup.select(".resinfo")
		self.getPhones(sidebar)
		self.getAddress(sidebar)
		self.geoLocation()
		self.activityCounts(sidebar)
		self.cuisines(sidebar)
		self.otherDetails(sidebar)

	def getPhones(self, sidebar):
		self.phones = ''
		for phone in sidebar.select(".resinfo .phone .res-tel span span"):
			self.phones += phone.get_text() + ","

	def getAddress(self, sidebar):
		address = sidebar.select(".res-main-address-text")
		self.full_address = address.select("span:nth-of-type(1)")[0].get_text()
		self.street = address.select('[itemprop="streetAddress"]')[0].get_text()
		self.region = address.select('[itemprop="addressRegion"]')[0].get_text()
		self.country = address.select('[itemprop="addressCountry"]')[0].get_text()

	def geoLocation(self):
		self.latitude = self.soup.select('meta [property=place:location:latitude]')[0]["content"]
		self.longitude = self.soup.select('meta [property=place:location:longitude]')[0]["content"]

	def activityCounts(self, sidebar):
		if len(sidebar.select('.res-stats-cont')) > 0 :
			self.review_count = self.toNum(sidebar.select(".res-main-stats-stat .res-main-stats-num")[0].get_text())
			self.photo_count = self.toNum(sidebar.select(".photocount .res-main-stats-num")[0].get_text())
			self.bookmarks_count = self.toNum(sidebar.select(".wishlist .res-main-stats-num")[0].get_text())
			self.checkin_count = self.toNum(sidebar.select(".beenthere .res-main-stats-num")[0].get_text())

	def cuisines(self, sidebar):
		self.cuisines = sidebar.select(".res-info-cuisines")[0].get_text()
		known_for = sidebar.select('.res-info-known-for-text')
		if len(known_for) > 0 :
			self.known_for = known_for[0].get_text()

	def otherDetails(self, sidebar):
		self.opening_hours = str(sidebar.select("#res-week-timetable")[0])
		self.highlights = str(sidebar.select(".res-info-highlights")[0])
		self.payment_methods = str(sidebar.select(".res-info-cft-text")[0])
		self.average_cost = sidebar.select('.res-info-group [itemprop="priceRange"]')[0].get_text()

	def getMenu(self):
		self.menu_urls = []
		menus = self.soup.select('.menu-preview__item img')
		if len(menu) > 0:
			for menu in menus:
				self.menu_urls.push(menu['src'])




