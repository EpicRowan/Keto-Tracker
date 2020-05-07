"""Models and database functions for Keto tracker project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email}>"


class Food(db.Model):
    """Movie on ratings website."""

    __tablename__ = "foods"

    food_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    name = db.Column(db.String(100))
    carbs = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Food food_id={self.food_id} name={self.name}>"


class Meal(db.Model):
    """Rating of a movie by a user."""

    __tablename__ = "meals"

    meal_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    meal_type = db.Column(db.String(100))
    food_id = db.Column(db.Integer, db.ForeignKey('foods.food_id'))
    date = db.Column(db.Integer, db.relationship("User",
                           backref=db.backref("meals",
                                              order_by=meal_id)))
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<meal_id={self.meal_id} 
                   movie_id={self.movie_id} 
                   user_id={self.user_id} 
                   score={self.score}>"""


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///carbs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")