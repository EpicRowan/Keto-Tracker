import datetime
from sqlalchemy import func

from model import User, Food, Meal, connect_to_db, db
from server import app


def load_users(user_filename):
    """Load users from u.user into database."""

    print("Users")

    for i, row in enumerate(open(user_filename)):
        row = row.rstrip()
        user_id, email, password = row.split("|")

        user = User(email=email,
                    password=password)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()


def load_food(food_filename):
    """Load movies from u.item into database."""

    print("Food")

    for i, row in enumerate(open(food_filename)):
        row = row.rstrip()

        # clever -- we can unpack part of the row!
        # movie_id, title, released_str, junk, imdb_url = row.split("|")[:5]

        # The date is in the file as daynum-month_abbreviation-year;
        # we need to convert it to an actual datetime object.

        # if released_str:
        #     released_at = datetime.datetime.strptime(released_str, "%d-%b-%Y")
        # else:
        #     released_at = None

        # Remove the (YEAR) from the end of the title.

        # title = title[:-7]   # " (YEAR)" == 7

        food = Food(name=name,
                    carbs=carbs)

        # We need to add to the session or it won't ever be stored
        db.session.add(food)

        # provide some sense of progress
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()


def load_meals(meals_filename):
    """Load ratings from u.data into database."""

    print("Meals")

    for i, row in enumerate(open(meals_filename)):
        row = row.rstrip()

        # user_id, movie_id, score, timestamp = row.split("\t")

        # user_id = int(user_id)
        # movie_id = int(movie_id)
        # score = int(score)

        # We don't care about the timestamp, so we'll ignore this

        meal = Meal(user_id=user_id,)

        # We need to add to the session or it won't ever be stored
        db.session.add(meal)

        # provide some sense of progress
        if i % 1000 == 0:
            print(i)

            # An optimization: if we commit after every add, the database
            # will do a lot of work committing each record. However, if we
            # wait until the end, on computers with smaller amounts of
            # memory, it might thrash around. By committing every 1,000th
            # add, we'll strike a good balance.

            db.session.commit()

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    user_filename = "seed_data/u.user"
    food_filename = ""
    meal_filename = ""
    load_users(user_filename)
    load_foods(food_filename)
    load_meals(meal_filename)
    set_val_user_id()