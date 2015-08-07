from app import db

# class Art(db.Model):
# 	__tablename__ = 'art'
# 	id = db.Column(db.Integer, primary_key=True)
# 	image_path = db.Column(db.String(300), unique=True)
# 	title = db.Column(db.String(500))

# 	responses = db.relationship('Response', backref = db.backref('art'))

# 	def __init__(self, image_path, title):
# 		self.image_path = image_path
# 		self.title = title

# 	def __repr__(self):
# 		return '<ID: {0} Path: {1}>'.format(self.id, self.image_path)

class Assignment(db.Model):
	__tablename__ = 'assignment'

	assignment_id = db.Column(db.Integer, primary_key = True)
	session_id = db.Column(db.String(300))
	user_id = db.Column(db.String(300))
	time = db.Column(db.String(300))
	seed = db.Column(db.Integer)
	outcome = db.Column(db.String(300))
	round_num = db.Column(db.Integer)

	def __init__(self, session_id, user_id, 
		time, seed, outcome, round_num):
		self.session_id = session_id
		self.user_id = user_id
		self.time = time
		self.seed = seed
		self.outcome = outcome
		self.round_num = round_num

	def __repr__(self):
		return '<ID: %r>' % self.assignment_id

class Response(db.Model):
	__tablename__ = 'response'

	response_id = db.Column(db.Integer, primary_key = True)
	session_id = db.Column(db.String(300))
	user_id = db.Column(db.String(300))
	time = db.Column(db.String(300))
	round_num = db.Column(db.Integer)
	winner = db.Column(db.String(300))
	fav_trump = db.Column(db.String(300))
	fav_bush = db.Column(db.String(300))
	fav_walker = db.Column(db.String(300))
	fav_carson = db.Column(db.String(300))
	fav_huckabee = db.Column(db.String(300))
	fav_cruz = db.Column(db.String(300))
	fav_rubio = db.Column(db.String(300))
	fav_paul = db.Column(db.String(300))
	fav_christie = db.Column(db.String(300))
	fav_kasich = db.Column(db.String(300))


	# user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

	def __init__(self, session_id, time, user_id, round_num, winner,
		fav_trump, fav_bush, fav_walker, fav_carson, fav_huckabee, 
		fav_cruz, fav_rubio, fav_paul, fav_christie, fav_kasich):

		self.session_id = session_id
		self.time = time
		self.user_id = user_id
		self.round_num = round_num
		self.winner = winner
		self.fav_trump = fav_trump
		self.fav_bush = fav_bush
		self.fav_walker = fav_walker
		self.fav_carson = fav_carson
		self.fav_huckabee = fav_huckabee
		self.fav_cruz = fav_cruz
		self.fav_rubio = fav_rubio
		self.fav_paul = fav_paul
		self.fav_christie = fav_christie
		self.fav_kasich = fav_kasich

	def __repr__(self):
		return '<ID: %r>' % self.response_id

class User(db.Model):
	__tablename__ = 'user'

	name = db.Column(db.String, primary_key=True)
	authenticated = db.Column(db.Boolean, default=True)

	def is_active(self):
		"""True, as all users are active."""
		return True

	def get_id(self):
		"""Return the email address to satify Flask-Login's requirements."""
		return self.name

	def is_authenticated(self):
		"""Return True if the user is authenticated."""
		return True

	def is_anonymous(self):
		"""False, as anonymous users aren't supported."""
		return False

	# __tablename__ = 'user'
	# user_id = db.Column(db.Integer, primary_key=True)
	# email = db.Column(db.String(120), unique=True)
	# password = db.Column(db.String)

	# responses = db.relationship('Response', backref = db.backref('user'))

	def __init__(self, name):

		self.name = name

	def is_authenticated(self):
	    return True

	def is_active(self):
	    return True

	def is_anonymous(self):
	    return False

	def get_id(self):
	    try:
	        return unicode(self.name)  # python 2
	    except NameError:
	        return str(self.name)  # python 3

	def __repr__(self):
	    return '<User %r>' % (self.name)
