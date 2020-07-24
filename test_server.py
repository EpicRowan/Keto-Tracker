import unittest 
from server import app 
from model import db, connect_to_db, example_data

class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes."""
    
        def setUp(self):
      """Stuff to do before every test."""

      self.client = app.test_client()
      app.config['TESTING'] = True

      # Connect to test database
      connect_to_db(app,"postgresql:///testdb")

      # Create tables and add sample data
      db.create_all()
      example_data()

    def tearDown(self):
    	"""Stuff to do after each test."""


    def test_home(self):
        """Make sure home page returns correct HTML."""

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
	unittest.main()
