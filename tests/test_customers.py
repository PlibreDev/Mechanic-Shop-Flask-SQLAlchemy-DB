from app import create_app
from app.models import db, Customer
from app.utils.util import encode_token
from datetime import datetime
import unittest


class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # Create test customer
            self.customer = Customer()
            self.customer.name = "Test User"
            self.customer.email = "test@email.com"
            self.customer.phone = "123-456-7890"
            self.customer.password = "testpassword"
            
            db.session.add(self.customer)
            db.session.commit()
            
        self.token = encode_token(1)
        self.client = self.app.test_client()

    def test_create_customer(self):
        """Test creating a new customer"""
        customer_payload = {
            "name": "John Doe",
            "email": "johndoe@email.com",
            "phone": "555-123-4567",
            "password": "password123"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], "John Doe")
        self.assertEqual(response.get_json()['email'], "johndoe@email.com")

    def test_invalid_customer_creation(self):
        """Test creating customer with missing required fields"""
        customer_payload = {
            "name": "John Doe",
            "phone": "555-123-4567",
            "password": "password123"
            # Missing email field
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)

    def test_duplicate_email_creation(self):
        """Test creating customer with duplicate email"""
        customer_payload = {
            "name": "Another User",
            "email": "test@email.com",  # Same as setUp customer
            "phone": "555-999-8888",
            "password": "password123"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], "Email already exists")

    def test_get_customers(self):
        """Test retrieving all customers"""
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.get_json(), list))

    def test_get_customer_by_id(self):
        """Test retrieving a specific customer by ID"""
        response = self.client.get('/customers/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], "Test User")

    def test_get_nonexistent_customer(self):
        """Test retrieving a customer that doesn't exist"""
        response = self.client.get('/customers/999')
        self.assertEqual(response.status_code, 404)

    def test_login_customer(self):
        """Test customer login with valid credentials"""
        credentials = {
            "email": "test@email.com",
            "password": "testpassword"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'success')
        self.assertIn('auth_token', response.get_json())
        return response.get_json()['auth_token']

    def test_invalid_login(self):
        """Test customer login with invalid credentials"""
        credentials = {
            "email": "wrong@email.com",
            "password": "wrongpassword"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['messages'], "Invalid username or password")

    def test_update_customer(self):
        """Test updating customer information"""
        update_payload = {
            "name": "Updated Name",
            "phone": "999-888-7777"
        }

        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.put('/customers/1', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Updated Name')
        self.assertEqual(response.get_json()['phone'], '999-888-7777')

    def test_update_customer_unauthorized(self):
        """Test updating customer without proper authorization"""
        update_payload = {
            "name": "Updated Name"
        }

        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.put('/customers/2', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_update_customer_no_token(self):
        """Test updating customer without token"""
        update_payload = {
            "name": "Updated Name"
        }

        response = self.client.put('/customers/1', json=update_payload)
        self.assertEqual(response.status_code, 401)

    def test_delete_customer(self):
        """Test deleting a customer"""
        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.delete('/customers/1', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], "Customer deleted successfully")

    def test_delete_customer_unauthorized(self):
        """Test deleting customer without proper authorization"""
        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.delete('/customers/2', headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_get_my_tickets(self):
        """Test retrieving customer's service tickets"""
        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.get('/customers/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.get_json(), list))


if __name__ == '__main__':
    unittest.main()
