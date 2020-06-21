import requests

import config

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Meal, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "megasecret"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
	"""Homepage."""
	user_id = session.get("user_id")
	if user_id:
		return redirect(f"/users/{user_id}")

	print(session)
	return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
	"""Show form for user signup."""

	return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
	"""Process registration."""

	# Get form variables
	email = request.form["email"]
	password = request.form["password"]

	if User.query.filter_by(email=email).first():
		flash("An account with this email address already exists.")
		return redirect("/register")

	new_user = User(email=email, password=password)

	db.session.add(new_user)
	db.session.commit()

	# session["user_id"] = user_id

	flash(f"User {email} added.")
	return redirect(f"/login")


@app.route('/login', methods=['GET'])
def login_form():
	"""Show login form."""

	return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
	"""Process login."""

	# Get form variables
	email = request.form["email"]
	password = request.form["password"]

	user = User.query.filter_by(email=email).first()

	if not user:
		flash("No such user", 'error')
		return redirect("/login")

	if user.password != password:
		flash("Incorrect password", 'error')
		return redirect("/login")

	session["user_id"] = user.user_id

	flash("Logged in")
	return redirect(f"/users/{user.user_id}")


@app.route("/users/<int:user_id>")
def user_detail(user_id):
	"""Show user's page"""

	user = User.query.get(user_id)
	meals = Meal.query.filter_by(user_id=user_id).all()

	return render_template("user.html", user_id=user_id, user=user, meals=meals)


@app.route('/users/<int:user_id>/new', methods=['GET'])
def new_food_entry_form(user_id):
	"""Show form for user's new entry."""
	
	return render_template("entry.html", user_id=user_id)


@app.route('/users/<int:user_id>/new', methods=['POST'])
def new_entry(user_id):
	"""Process new food entry."""


		#  Get form variables
	user_id = session["user_id"] 
	food = request.form["food"]
	carbs = request.form["carbs"]
	date = request.form["date"]
	

	new_meal = Meal(user_id=user_id,food=food, carbs=carbs, date=date)

	db.session.add(new_meal)
	db.session.commit()
	
		
	return redirect(f"/users/{user_id}")

@app.route('/search')
def search():
	"""Redirect to Edam food API search"""


	return render_template('search.html')


@app.route('/search_results', methods=["POST"])
def search_results():
	"""Search the Edam food API for food name and carb count"""

	searched=request.form["searched"]
	params = searched.replace(" ", "%20")
	res = requests.get(f'https://api.edamam.com/api/food-database/v2/parser?ingr={params}&app_id={config.app_id}&app_key={config.api_key}')
	search_results = res.json()
	foods = {}
	i = 0
	for item in search_results.values():
		foods.update([(search_results["hints"][i]["food"]["label"], search_results["hints"][i]["food"]["nutrients"]["CHOCDF"])])
		i+=1
		
	return render_template('search_results.html', foods=foods)


@app.route('/logout')
def logout():
	"""Log out."""

	del session["user_id"]
	flash("Logged Out")
	return redirect("/")


if __name__ == "__main__":
	# We have to set debug=True here, since it has to be True at the
	# point that we invoke the DebugToolbarExtension
	app.debug = True
	# make sure templates, etc. are not cached in debug mode
	app.jinja_env.auto_reload = app.debug

	connect_to_db(app)

	# Use the DebugToolbar
	DebugToolbarExtension(app)

	app.run(port=5000, host='0.0.0.0')