from flask import Flask, request, render_template #import flask
from flask import send_from_directory

import os


# from flask_admin import Admin
# from flask_admin.contrib.peewee import ModelView

from models import Post
import post_db


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'images')

# UPLOAD_FOLDER = '/images'


app = Flask(__name__)	# ceate an instance of Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = '123456790'

# admin = Admin(app, name='microblog', template_mode='bootstrap3')
# admin.add_view(ModelView(Post))



@app.route('/') # the route decorator binds a function to a url
def home_page():
	post_list = post_db.select_page()
	return render_template('index.html', post_list=post_list)


@app.route('/page/<pageno>')
def get_page(page_no):
	post_db.select_page(page_no)
	return "Success"


@app.route('/api/delete/<post_id>', methods=['POST'])
def delete_post(post_id):
	post_db.delete_article(post_id)
	return "Success"

@app.route('/api/images/<filename>')
def get_image(filename):
	print "This is my filename ", filename
	print app.config['UPLOAD_FOLDER']
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/insert', methods=['GET', 'POST'])
def insert_post():

	if request.method == 'POST':
		post_db.insert_article(request)

	else:
		new_request = {}
		new_request.title = 'My new post title'
		new_request.body = 'My new post body'
		new_request.link = 'https://github.com/manny1995'
		post_db.insert_article(new_request)

	return "Success"



if __name__ == '__main__':
	print "ad"
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)




