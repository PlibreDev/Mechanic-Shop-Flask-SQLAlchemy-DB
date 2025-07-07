from app import create_app
from app.models import db, Mechanic
import unittest


class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # Create test mechanic
            self.mechanic = Mechanic()
            self.mechanic.name = "Test Mechanic"
            self.mechanic.email = "mechanic@email.com"
            self.mechanic.phone = "555-123-4567"
            self.mechanic.salary = 50000.0
            
            db.session.add(self.mechanic)
            db.session.commit()
            
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        """Test creating a new mechanic"""
        mechanic_payload = {
            "name": "Jane Smith",
            "email": "jane@email.com",
            "phone": "555-987-6543",
            "salary": 55000.0
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], "Jane Smith")

    def test_invalid_mechanic_creation(self):
        """Test creating mechanic with missing required fields"""
        mechanic_payload = {
            "name": "Jane Smith",
            "phone": "555-987-6543",
            "salary": 55000.0
            # Missing email field
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)

    def test_get_mechanics(self):
        """Test retrieving all mechanics"""
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.get_json(), list))

    def test_get_mechanic_by_id(self):
        """Test retrieving a specific mechanic by ID"""
        response = self.client.get('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], "Test Mechanic")

    def test_get_nonexistent_mechanic(self):
        """Test retrieving a mechanic that doesn't exist"""
        response = self.client.get('/mechanics/999')
        self.assertEqual(response.status_code, 404)

    def test_update_mechanic(self):
        """Test updating mechanic information"""
        update_payload = {
            "name": "Updated Mechanic",
            "salary": 60000.0
        }

        response = self.client.put('/mechanics/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Updated Mechanic')
        self.assertEqual(response.get_json()['salary'], 60000.0)

    def test_update_nonexistent_mechanic(self):
        """Test updating a mechanic that doesn't exist"""
        update_payload = {
            "name": "Updated Mechanic"
        }

        response = self.client.put('/mechanics/999', json=update_payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_mechanic(self):
        """Test deleting a mechanic"""
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], "Mechanic deleted successfully")

    def test_delete_nonexistent_mechanic(self):
        """Test deleting a mechanic that doesn't exist"""
        response = self.client.delete('/mechanics/999')
        self.assertEqual(response.status_code, 404)

    def test_most_active_mechanics(self):
        """Test getting most active mechanics"""
        response = self.client.get('/mechanics/most-active')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.get_json(), list))


if __name__ == '__main__':
    unittest.main()
