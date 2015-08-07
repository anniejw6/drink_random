from flask import (render_template, Flask, request,
	flash, session, redirect, url_for, g)
from app import app, forms, models, db, lm, bcrypt
from random import randint
import random
from sqlalchemy import func
import pandas as pd
from flask.ext.login import (LoginManager, login_required, login_user,
	logout_user, current_user)
import json
from flask.ext.bcrypt import Bcrypt
import logging
import uuid
import sys
from numpy.random import RandomState
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, SelectField

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)
lm.login_view = 'login'

@lm.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    #return models.User.query.filter_by(email = user_id).first()
    return models.User.query.get(user_id)

def randShots(seed):

	prng = RandomState(seed)
	treat = prng.randint(0, 2)
	if treat == 1:
		return('1 Shot')
	else:
		return(str(treat) + ' Shots')

# before request
@app.before_request
def before_request():

	if 'round' not in session:
		session['round'] = 0

	if 'session_idd' not in session:
		session['session_idd'] = uuid.uuid4().hex

	if current_user.is_authenticated():
		session['user_idd'] = session['user_id']
	else:
		session['user_idd'] = session['session_idd'] 

# Home Page
# Start New Round
@app.route('/', methods = ['GET', 'POST'])
@app.route('/index/', methods = ['GET', 'POST'])
@login_required
def index():

	app.logger.info(session['round'])

	return render_template('randomize_get.html')


@app.route('/drink/', methods = ['GET', 'POST'])
@login_required
def drink():

	app.logger.info(session['round'])

	# Generate Treatment
	time = datetime.utcnow()
	seed = time.microsecond
	assignment = randShots(seed)

	# Add Round
	session['round'] = (session['round'] + 1)

	# Record Things
	assign = models.Assignment(
		session_id = session['session_idd'],
		user_id = session['user_idd'],
		time = str(time),
		seed = seed,
		outcome = assignment,
		round_num = session['round'])
	db.session.add(assign)
	db.session.commit()

	return render_template('randomize_post.html', treat = assignment)


# Record Errors
@app.route('/record/', methods = ['GET', 'POST'])
@login_required
def record():

	# Create Form for Favorability
	choices_winner = [('trump', 'Donald Trump'), ('bush', 'Jeb Bush'), ('walker', 'Scott Walker'),
		('carson', 'Ben Carson'), ('huckabee', 'Mike Huckabee'), ('cruz', 'Ted Cruz'), ('rubio', 'Marco Rubio'),
		('paul', 'Rand Paul'), ('christie', 'Chris Christie'), ('kasich', 'John Kasich')]
	random.shuffle(choices_winner)

	class Submission(Form):
		winner = SelectField('winner', choices = choices_winner)
		submit = SubmitField("Submit")

	attributes = [('Donald Trump', 'fav_trump'), ('Jeb Bush', 'fav_bush'), 
	('Scott Walker', 'fav_walker'), ('Ben Carson', 'fav_carson'), 
	('Mike Huckabee', 'fav_huckabee'), ('Ted Cruz', 'fav_cruz'), 
	('Marco Rubio', 'fav_rubio'), ('Ron Paul', 'fav_paul'), 
	('Chris Christie', 'fav_christie'), ('John Kasich', 'fav_kasich')]
	random.shuffle(attributes)

	for label, name in attributes:
		setattr(Submission, name, SelectField(label, choices = [('1', 'Very Positive'), ('2', 'Somewhat Positive'),
		('3', 'Neither Positive nor Negative'), ('4', 'Somewhat Negative'), ('5', 'Very Negative')], default = '3'))

	sub = Submission()

	if sub.validate_on_submit():

		time = str(datetime.utcnow())
		app.logger.info(sub.winner.data)
		app.logger.info(sub.fav_trump.data)

		response = models.Response(
			session_id = session['session_idd'], 
			time = time,
			user_id = session['user_idd'], 
			winner = sub.winner.data,
			round_num = session['round'],
			fav_trump = sub.fav_trump.data, 
			fav_bush = sub.fav_bush.data, 
			fav_walker = sub.fav_walker.data, 
			fav_carson = sub.fav_carson.data, 
			fav_huckabee = sub.fav_huckabee.data, 
			fav_cruz = sub.fav_cruz.data, 
			fav_rubio = sub.fav_rubio.data, 
			fav_paul = sub.fav_paul.data, 
			fav_christie = sub.fav_christie.data, 
			fav_kasich = sub.fav_kasich.data)

		db.session.add(response)
		db.session.commit()

		return redirect(url_for('index'))

	return render_template('record.html', form = sub)

# Log-In & Register
@app.route("/login/", methods=["GET", "POST"])
def login():
	"""For GET requests, display the login form. 

	For POSTS, login the current user by processing the form."""

	form = forms.LoginForm()
	#app.logger.info(session['user_id'])

	if form.validate_on_submit():

		# Try to find user
		user = models.User.query.filter_by(name = form.name.data).first()
		app.logger.info(user)
		# If it exists, log in
		if user:

			user.authenticated = True
			app.logger.info('logged')
		# If it doesn't exist, register and log in
		else: 
			app.logger.info('registered')
			user = models.User(request.form['name'])
			db.session.add(user)
			db.session.commit()

		login_user(user, remember=True)
		session['user_idd'] = session['user_id']
		flash('User successfully registered')

		#app.logger.info(current_user)
		#app.logger.info(session['user_id'])

		return redirect(url_for("index"))

	return render_template("reg_login.html", form=form)

# Put responses in database
# @app.route('/submission/', methods=['POST', 'GET'])
# def submission():

# 	app.logger.info(request.form)

# 	time = str(datetime.utcnow())

# 	response = models.Response(
# 		session_id = session['session_idd'], 
# 		time = time,
# 		user_id = session['user_idd'], 
# 		republican = int(request.form['republican']),
# 		round_num = session['round'])

# 	app.logger.info('test')

# 	db.session.add(response)
# 	db.session.commit()

# 	app.logger.info('added')

# 	return redirect(url_for("index"))

# Logout User
@app.route("/logout/", methods=["GET"])
@login_required
def logout():
	"""Logout the current user."""
	user = current_user
	user.authenticated = False
	db.session.add(user)
	db.session.commit()
	logout_user()
	session['user_idd'] = session['session_idd']
	session['round'] = 0
	return redirect(url_for("index"))