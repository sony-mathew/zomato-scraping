# from library.country import *
from library.city import *
from library.database import *
import time
import sys

#scrape teh countries
# x = ScrapeCountry();

# #scrape the base city pages
# for city in City.select().where(City.crawled == False):
# 	name = city.name.decode('unicode_escape')
# 	link = city.link.decode('unicode_escape')
# 	sys.stdout.write("Crawling : " + name.encode('utf-8') + ", " + link.encode('utf-8') + "\n")
# 	y = ScrapeCityBasePage(city);
# 	# time.sleep(1)


for city in City.select().where(City.finished == False):
	name = city.name.decode('unicode_escape')
	link = city.link.decode('unicode_escape')
	sys.stdout.write("Crawling : " + name.encode('utf-8') + ", " + link.encode('utf-8') + "\n")
	
	if city.pages == 1 :
		city.finished = True
		city.save()

	for page in range(city.pages_crawled + 1, city.pages + 1):
		sys.stdout.write("Page Number : " + str(page) + " ")
		y = ScrapeCityBasePage(city, city.link + "?pages" + str(page))