from common import *
from database import * 
from links import * 
import sys

class ScrapeCountry(CommonBasics):

	def __init__(self):
		self.c_link = Links.baseDirectory
		self.scrape(self.c_link)
		self.parseContent()

	def parseContent(self):
		main_container = self.soup.select('.container')[0]
		container_content = main_container.get_text()
		container_hash = self.get_hash(container_content)

		#insert in source
		source_id = self.insert_source(self.c_link, container_hash)

		countries = main_container.select('.country-city-container')
		for country in countries:
			self.parseCountry(country, source_id)

	def parseCountry(self, country, source_id):
		#name, link, hash
		country_name = self.sterilize(country.select('a h1')[0].get_text(), [" "])
		country_link = self.sterilize(country.select('a:nth-of-type(1)')[0].get('href'), [" "])
		country_hash = self.get_hash(country.get_text())
		sys.stdout.write("Country : " + country_name + "\n")
		#insert into country
		country_id = self.db_insert_country(source_id, country_name, country_link, country_hash)

		cities = country.select('dt')
		for city in cities:
			self.parseCities(city, country_id, source_id)

	def parseCities(self, city, country_id, source_id):
		el = city.select('a')[0]
		#name, link
		city_name = self.sterilize(el.get_text(), [" "])
		city_link = self.sterilize(el.get('href').replace("directory", "restaurants"), [" "])
		#insert into city
		self.db_insert_city(source_id, country_id, city_name, city_link)

	def db_insert_country(self, source, name, link, hash_):
		new_country = Country.create(source=source, name=name, link=link, hash_md5=hash_)
		return new_country.id

	def db_insert_city(self, source, country, name, link):
		City.create(source=source, country=country, name=name, link=link)
