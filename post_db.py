from models import Post, setup, teardown
import peewee
import uuid
import urllib
import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

PAGE_SIZE = 3

from flask import current_app as app

def insert_article(request):

	imageFile = request.files['imageFile']
	print app.config['UPLOAD_FOLDER']

	filename = str(uuid.uuid1()) + '.png'
	localLink = os.path.join(APP_ROOT + '/images/' + filename)
	apiLink = '/api/images/' + filename
	imageFile.save(localLink)
	newPost = Post.create(title=request.form['title'], body=request.form['body'], image=apiLink, link=request.form['link'])
	newPost.save()
	teardown()


def delete_article(post_id):
	delete_query = Post.delete().where(Post.id == post_id)
	delete_query.execute()
	teardown()


def select_article(page_no):
	print (page_no)

def has_prev(current_page):
	return current_page > 1

def has_next(current_page):
	post_list = Post.select().order_by(Post.id.desc()).paginate(current_page + 2, PAGE_SIZE)

	return len(post_list) > 0


def select_page(offset=0):
	offset = int(offset)
	post_list = Post.select().order_by(Post.id.desc()).paginate(offset, PAGE_SIZE)
	teardown()
	return post_list


