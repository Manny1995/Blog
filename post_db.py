from models import Post, setup, teardown
import peewee
import uuid
import urllib
import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


from flask import current_app as app

def insert_article(request):

	imageFile = request.files['imageFile']
	print app.config['UPLOAD_FOLDER']

	filename = str(uuid.uuid1()) + '.png'
	localLink = os.path.join(APP_ROOT + '/images/' + filename)
	apiLink = '/api/images/' + filename
	imageFile.save(localLink)
	# newLink = urllib.pathname2url(newLink)
	# newLink = '/api' + newLink
	# print "encoded url is ", newLink
	newPost = Post.create(title=request.form['title'], body=request.form['body'], image=apiLink, link=request.form['link'])
	newPost.save()
	teardown()


def delete_article(post_id):
	delete_query = Post.delete().where(Post.id == post_id)
	delete_query.execute()
	teardown()


def select_article(page_no):
	print (page_no)



def select_page(offset=0):
	offset = int(offset) 
	post_list = Post.select().paginate(offset, 4)
	teardown()
	return post_list


