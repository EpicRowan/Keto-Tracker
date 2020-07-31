import unittest 
from server import app 
from model import db, connect_to_db, example_data, User
from flask import session

app.secret_key = "megasecret"

class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
      """Stuff to do after each test."""


    def test_home(self):
        """Make sure home page returns correct HTML."""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)

    def test_register_form(self):
        """Show form for user signup."""
        
        result = self.client.get('/register')
        self.assertIn(b'Register', result.data)


    def test_login_form(self):
        """Show login form."""
   
        result = self.client.get('/')
        self.assertIn(b'Login', result.data)


    def test_login_process(self):
        """Process login."""

        result = self.client.post("/login",
                                  data={"email": "rachel@rachel.com", "password": "123"},
                                  follow_redirects=True)
        self.assertIn(b"Welcome rachel@rachel.com", result.data)


    def test_register_process(self):
        """Process registration."""
        result = self.client.post("/register",
                                  data={"email": "joe@joe.com", "password": "123"},
                                  follow_redirects=True)
        self.assertIn(b"User joe@joe.com added.", result.data)

  
    def test_user_detail(self, user_id=1):
        """Show user's page"""
        # user = User.query.get(user_id)
        # print(user)
        # result = self.client.get("/users/1", user=user)
        

        data = {"user_id": 1}
        result = self.client.get("/users/1", data=data)
        user = User.query.get(1)
        print(user)
        self.assertEqual(result.status_code, 200)

class FlaskTestsLoggedIn(unittest.TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1


    def test_logout(self):
        """Log out."""
    
        result = self.client.get("/logout",follow_redirects=True)
      
        self.assertIn(b'Logged Out', result.data)


    # def test_user_detail(self):
    #     """Show user's page"""

    #     result = self.client.get("/users/1")
    #     self.assertIn(b"Welcome rachel@rachel.com", result.data)

    # @app.route("/users/<int:user_id>")
    # def test_user_detail(self):
    # """Show user's page"""

    # user = User.query.get(user_id)
    # meals = Meal.query.filter_by(user_id=user_id).all()

    # return render_template("user.html", user_id=user_id, user=user, meals=meals)


    # @app.route('/users/<int:user_id>/new', methods=['GET'])
    # def test_new_food_entry_form(self):
    # """Show form for user's new entry."""
    
    # return render_template("entry.html", user_id=user_id)


    # @app.route('/users/<int:user_id>/new', methods=['POST'])
    # def test_new_entry(self):
    # """Process new food entry."""


    #   #  Get form variables
    # user_id = session["user_id"] 
    # food = request.form["food"]
    # carbs = request.form["carbs"]
    # date = request.form["date"]
    

    # new_meal = Meal(user_id=user_id,food=food, carbs=carbs, date=date)

    # db.session.add(new_meal)
    # db.session.commit()
    
        
    # return redirect(f"/users/{user_id}")

    # @app.route('/search')
    # def test_search(self):
    # """Redirect to Edam food API search"""


    # return render_template('search.html')


    # @app.route('/search_results', methods=["POST"])
    # def test_search_results(self):
    # """Search the Edam food API for food name and carb count"""

    # searched=request.form["searched"]
    # params = searched.replace(" ", "%20")
    # res = requests.get(f'https://api.edamam.com/api/food-database/v2/parser?ingr={params}&app_id={config.app_id}&app_key={config.api_key}')
    # search_results = res.json()
    # foods = {}
    # i = 0
    # for item in search_results.values():
    #   foods.update([(search_results["hints"][i]["food"]["label"], search_results["hints"][i]["food"]["nutrients"]["CHOCDF"])])
    #   i+=1
        
    # return render_template('search_results.html', foods=foods)



if __name__ == '__main__':
    unittest.main()
