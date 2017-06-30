from peewee import *
import sqlite3
from sqlite3 import Error
import datetime as dt

# db = SqliteDatabase('microblog.db')

db = SqliteDatabase('microblog.db', check_same_thread=False)

def setup():
	db.connect()

def teardown():
	if not db.is_closed():
		db.close()



class Post(Model):
	title = CharField()
	image = CharField()
	date = DateField(default=dt.datetime.now)
	body = TextField()
	link = CharField()

	class Meta:
		database = db



db.create_tables([Post], safe=True)
