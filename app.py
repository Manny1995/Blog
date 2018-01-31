# Created by Immanuel Amirtharaj

from flask import Flask, request, render_template
from flask import send_from_directory
from flask import redirect

import os


from models import Post
import post_db


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'images')


app = Flask(__name__)	# ceate an instance of Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/') # the route decorator binds a function to a url
def home_page():
	post_list = post_db.select_page()
	return redirect('/page/1')


@app.route('/login', methods=['GET', 'POST'])
def login():

	if request.method == 'GET':
		return render_template('login.html')

	else:
		username = request.form['username']
		password = request.form['password']
		return redirect('/', code=302)


@app.route('/page/<page_no>')
def get_page(page_no):
	page_no = int(page_no)
	post_list = post_db.select_page(page_no)
	
	prev_link = '/page/' + str(page_no - 1)
	next_link = '/page/' + str(page_no + 1)

	has_next = post_db.has_next(page_no)
	has_prev = post_db.has_prev(page_no)

	if has_prev == False:
		prev_link = None

	if has_next == False:
		next_link = None

	return render_template('index.html', post_list=post_list, next_link=next_link, prev_link=prev_link)


@app.route('/posts/new', methods=['GET', 'POST'])
def insert_post():
	post_db.insert_article(request)
	return "success"

@app.route('/api/images/<filename>')
def get_image(filename):
	print app.config['UPLOAD_FOLDER']
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def main():
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
	main()

