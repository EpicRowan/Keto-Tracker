import unittest 
from server import app
from model import db, connect_to_db, example_data, User
from flask import session


app.secret_key = "megasecret"

class BasicTests(unittest.TestCase):
    """Test routes that don't require access to the database or session."""

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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


    def test_new_food_entry_form(self):
        """Show form for user's new entry."""

        result = self.client.get('/users/1/new')
        self.assertEqual(result.status_code, 200)

    def test_search(self):
        """Redirect to Edam food API search"""

        result = self.client.get("/search",
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)


class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes that require access to the database."""

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


    def test_login_process(self):
        """Process login."""

        result = self.client.post("/login",
                                  data={"email": "rachel@rachel.com", "password": "123"},
                                  follow_redirects=True)
        self.assertIn(b"Welcome rachel@rachel.com", result.data)


    def test_register_process(self):
        """Process registration."""
        result = self.client.post("/register",
                                  data={"user_id": 3,"email": "joe@joe.com", "password": "123"},
                                  follow_redirects=True)
        self.assertIn(b"User joe@joe.com added.", result.data)

  
    def test_user_detail(self):
        """Show user's page"""   

        user = User.query.get(1)
        result = self.client.get("/users/1")

        self.assertIn(b"Welcome rachel@rachel.com", result.data)
        self.assertIn(b"pie", result.data)


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

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def test_logout(self):
        """Log out."""
    
        result = self.client.get("/logout",follow_redirects=True)
      
        self.assertIn(b'Logged Out', result.data)

    
    def test_new_entry(self):
    # """Process new food entry."""

        result = self.client.post("/users/1/new",
                                  data={"food": "pizza", "carbs": 7, "date": "2020-02-02"},
                                  follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn(b"pizza", result.data)



    def test_search_results(self):
        """Search the Edam food API for food name and carb count"""

        result = self.client.post("/search_results",
                              data={"searched": "cookie"},
                              follow_redirects=True)
        self.assertEqual(result.status_code, 200)



if __name__ == '__main__':
    unittest.main()
