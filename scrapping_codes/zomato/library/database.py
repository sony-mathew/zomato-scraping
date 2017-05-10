from datetime import datetime
from peewee import *


mysql_db = MySQLDatabase('zomato', user='root', password='', host='' )

class BaseModel(Model):
	class Meta:
		database = mysql_db


class Source(BaseModel):
	link = TextField()
	hash_md5 = TextField()
	c_date = DateTimeField(default=datetime.now)



class Country(BaseModel):
	source = ForeignKeyField(Source, related_name='countries') 
	name = TextField()
	link = TextField()
	hash_md5 = TextField()



class City(BaseModel):
	source = ForeignKeyField(Source, related_name='cities')
	country = ForeignKeyField(Country, related_name='cities')
	name = TextField()
	link = TextField()
	pages = IntegerField()
	crawled = BooleanField()
	pages_crawled = IntegerField()
	finished = BooleanField()

class Listing(BaseModel):
	city = ForeignKeyField(City, related_name='listings')
	name = TextField()
	address = TextField()
	cuisine = TextField()
	price_range = IntegerField()
	rating = TextField()
	voted_users = TextField()
	link = TextField()
	crawled = BooleanField()



