from app import create_app
from app.models import db, Inventory
import unittest


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # Create test part
            self.part = Inventory()
            self.part.name = "Test Part"
            self.part.price = 25.99
            
            db.session.add(self.part)
            db.session.commit()
            
        self.client = self.app.test_client()

    def test_create_inventory_part(self):
        """Test creating a new inventory part"""
        part_payload = {
            "name": "Brake Pad",
            "price": 45.99
        }

        response = self.client.post('/inventory/', json=part_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], "Brake Pad")
        self.assertEqual(response.get_json()['price'], 45.99)

    def test_invalid_inventory_creation(self):
        """Test creating inventory part with missing required fields"""
        part_payload = {
            "name": "Brake Pad"
            # Missing price field
        }

        response = self.client.post('/inventory/', json=part_payload)
        self.assertEqual(response.status_code, 400)

    def test_get_inventory(self):
        """Test retrieving all inventory parts"""
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.get_json(), list))

    def test_get_inventory_by_id(self):
        """Test retrieving a specific inventory part by ID"""
        response = self.client.get('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], "Test Part")

    def test_get_nonexistent_inventory(self):
        """Test retrieving an inventory part that doesn't exist"""
        response = self.client.get('/inventory/999')
        self.assertEqual(response.status_code, 404)

    def test_update_inventory(self):
        """Test updating inventory part information"""
        update_payload = {
            "name": "Updated Part",
            "price": 35.99
        }

        response = self.client.put('/inventory/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Updated Part')
        self.assertEqual(response.get_json()['price'], 35.99)

    def test_update_nonexistent_inventory(self):
        """Test updating an inventory part that doesn't exist"""
        update_payload = {
            "name": "Updated Part"
        }

        response = self.client.put('/inventory/999', json=update_payload)
        self.assertEqual(response.status_code, 404)

    def test_delete_inventory(self):
        """Test deleting an inventory part"""
        response = self.client.delete('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], "Part deleted successfully")

    def test_delete_nonexistent_inventory(self):
        """Test deleting an inventory part that doesn't exist"""
        response = self.client.delete('/inventory/999')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
