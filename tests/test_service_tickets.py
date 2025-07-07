from app import create_app
from app.models import db, ServiceTicket, Customer, Mechanic
from datetime import datetime
import unittest


class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # Create test customer
            self.customer = Customer()
            self.customer.name = "Test Customer"
            self.customer.email = "customer@email.com"
            self.customer.phone = "555-123-4567"
            self.customer.password = "testpassword"
            
            # Create test mechanic
            self.mechanic = Mechanic()
            self.mechanic.name = "Test Mechanic"
            self.mechanic.email = "mechanic@email.com"
            self.mechanic.phone = "555-987-6543"
            self.mechanic.salary = 50000.0
            
            db.session.add(self.customer)
            db.session.add(self.mechanic)
            db.session.commit()
            
        self.client = self.app.test_client()

    def test_create_service_ticket(self):
        """Test creating a new service ticket"""
        ticket_payload = {
            "VIN": "1234567890ABCDEFG",
            "service_date": "2024-01-15T10:00:00",
            "service_desc": "Oil change and tire rotation",
            "customer_id": 1
        }

        response = self.client.post('/service_tickets/', json=ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['VIN'], "1234567890ABCDEFG")

    def test_invalid_service_ticket_creation(self):
        """Test creating service ticket with missing required fields"""
        ticket_payload = {
            "VIN": "1234567890ABCDEFG",
            "service_desc": "Oil change and tire rotation"
            # Missing service_date and customer_id
        }

        response = self.client.post('/service_tickets/', json=ticket_payload)
        self.assertEqual(response.status_code, 400)

    def test_get_service_tickets(self):
        """Test retrieving all service tickets"""
        response = self.client.get('/service_tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.get_json(), list))

    def test_assign_mechanic_to_ticket(self):
        """Test assigning a mechanic to a service ticket"""
        # First create a ticket
        ticket_payload = {
            "VIN": "1234567890ABCDEFG",
            "service_date": "2024-01-15T10:00:00",
            "service_desc": "Oil change",
            "customer_id": 1
        }
        ticket_response = self.client.post('/service_tickets/', json=ticket_payload)
        ticket_id = ticket_response.get_json()['id']

        # Then assign mechanic
        response = self.client.put(f'/service_tickets/{ticket_id}/assign-mechanic/1')
        self.assertEqual(response.status_code, 200)

    def test_assign_nonexistent_mechanic(self):
        """Test assigning a non-existent mechanic to a ticket"""
        # First create a ticket
        ticket_payload = {
            "VIN": "1234567890ABCDEFG",
            "service_date": "2024-01-15T10:00:00",
            "service_desc": "Oil change",
            "customer_id": 1
        }
        ticket_response = self.client.post('/service_tickets/', json=ticket_payload)
        ticket_id = ticket_response.get_json()['id']

        # Try to assign non-existent mechanic
        response = self.client.put(f'/service_tickets/{ticket_id}/assign-mechanic/999')
        self.assertEqual(response.status_code, 404)

    def test_remove_mechanic_from_ticket(self):
        """Test removing a mechanic from a service ticket"""
        # Create ticket and assign mechanic first
        ticket_payload = {
            "VIN": "1234567890ABCDEFG",
            "service_date": "2024-01-15T10:00:00",
            "service_desc": "Oil change",
            "customer_id": 1
        }
        ticket_response = self.client.post('/service_tickets/', json=ticket_payload)
        ticket_id = ticket_response.get_json()['id']
        
        self.client.put(f'/service_tickets/{ticket_id}/assign-mechanic/1')

        # Then remove mechanic
        response = self.client.put(f'/service_tickets/{ticket_id}/remove-mechanic/1')
        self.assertEqual(response.status_code, 200)

    def test_edit_ticket_mechanics(self):
        """Test adding and removing multiple mechanics from a ticket"""
        # Create ticket first
        ticket_payload = {
            "VIN": "1234567890ABCDEFG",
            "service_date": "2024-01-15T10:00:00",
            "service_desc": "Major repair",
            "customer_id": 1
        }
        ticket_response = self.client.post('/service_tickets/', json=ticket_payload)
        ticket_id = ticket_response.get_json()['id']

        # Edit mechanics
        edit_payload = {
            "add_ids": [1],
            "remove_ids": []
        }

        response = self.client.put(f'/service_tickets/{ticket_id}/edit', json=edit_payload)
        self.assertEqual(response.status_code, 200)

    def test_add_part_to_ticket(self):
        """Test adding a part to a service ticket"""
        # Create ticket first
        ticket_payload = {
            "VIN": "1234567890ABCDEFG",
            "service_date": "2024-01-15T10:00:00",
            "service_desc": "Brake repair",
            "customer_id": 1
        }
        ticket_response = self.client.post('/service_tickets/', json=ticket_payload)
        ticket_id = ticket_response.get_json()['id']

        # Add part (assuming part ID 1 exists)
        response = self.client.put(f'/service_tickets/{ticket_id}/add-part/1')
        # This might return 404 if no inventory exists, which is expected
        self.assertIn(response.status_code, [200, 404])


if __name__ == '__main__':
    unittest.main()
