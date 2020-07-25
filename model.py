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
    """User of website."""

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
    """Food info from database"""

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
    """Meal info inputed by user"""

    __tablename__ = "meals"

    meal_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    food = db.Column(db.String(100))
    carbs = db.Column(db.Integer)
    user = db.relationship('User', backref=db.backref('meal'))
    date = db.Column(db.DateTime())


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data

    User.query.delete()
    Food.query.delete()
    Meal.query.delete()

    print('example_data')

    # Sample User table

    U1 = User(user_id =1, email='joe@joe.com', password ="123")
 
    # Sample Food 

    F1 = Food(building_id =1, name='MegaCorp', liquefaction='Very High', at_risk= True)

    # Sample Meal

    M1 = Meal(building_id=4, status="Seismic Retrofitted", liquefaction= "yes")
    

    db.session.add_all([U1, F1, M1])
    db.session.commit()    




    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<meal_id={self.meal_id} 
                   user_id={self.user_id}>"""


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