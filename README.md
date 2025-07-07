# Mechanic Shop API

A comprehensive Flask-based REST API for managing a mechanic shop's operations, including customer management, service tickets, mechanic assignments, and inventory tracking.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Database Schema](#database-schema)
- [Rate Limiting & Caching](#rate-limiting--caching)
- [Contributing](#contributing)

## Overview

The Mechanic Shop API is designed to streamline operations for automotive service businesses. It provides a complete backend solution for managing customers, mechanics, service tickets, and inventory with secure authentication, rate limiting, and comprehensive documentation.

## Features

### Core Functionality
- **Customer Management**: CRUD operations for customer accounts with secure authentication
- **Mechanic Management**: Track mechanic information and performance metrics
- **Service Tickets**: Manage service requests with mechanic assignments and part tracking
- **Inventory Management**: Track parts and supplies with pricing

### Security & Performance
- **JWT Authentication**: Secure token-based authentication for customer accounts
- **Rate Limiting**: Protection against API abuse with configurable limits
- **Caching**: Improved performance with Flask-Caching
- **Input Validation**: Comprehensive data validation using Marshmallow schemas

### Advanced Features
- **Many-to-Many Relationships**: Complex relationships between tickets, mechanics, and parts
- **Pagination**: Efficient data retrieval for large datasets
- **Advanced Queries**: Analytics like most active mechanics
- **Swagger Documentation**: Interactive API documentation
- **Comprehensive Testing**: Full test coverage with positive and negative test cases

## Project Structure

```
mechanic-shop-api/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── extensions.py               # Flask extensions initialization
│   ├── models.py                   # SQLAlchemy models
│   ├── blueprints/                 # Modular route organization
│   │   ├── customers/              # Customer-related endpoints
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── mechanics/              # Mechanic-related endpoints
│   │   ├── service_tickets/        # Service ticket endpoints
│   │   └── inventory/              # Inventory management
│   ├── static/                     # Static files
│   │   └── swagger.yaml            # Swagger API specification
│   └── utils/
│       └── util.py                 # Utility functions (JWT, decorators)
├── tests/                          # Comprehensive test suite
├── config.py                       # Configuration settings
├── app.py                          # Application entry point
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Installation

### Prerequisites
- Python 3.8+
- MySQL Server (for production) or SQLite (for testing)
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mechanic-shop-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   - For MySQL: Create a database named `mechanic_db`
   - Update database URL in `config.py` if needed

5. **Initialize the database**
   ```python
   from app import create_app
   from app.models import db
   
   app = create_app('DevelopmentConfig')
   with app.app_context():
       db.create_all()
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

## Configuration

The application supports multiple environments configured in `config.py`:

- **DevelopmentConfig**: MySQL database, debug mode enabled
- **TestingConfig**: SQLite database for isolated testing
- **ProductionConfig**: Production-ready settings (to be implemented)

### Environment Variables
Consider setting these environment variables for production:
- `SECRET_KEY`: JWT secret key
- `DATABASE_URL`: Database connection string

## API Documentation

### Interactive Documentation
Access the Swagger UI documentation at: `http://localhost:5000/api/docs/`

### Base URL
```
http://localhost:5000
```

### Available Endpoints

#### Customers (`/customers`)
- `POST /customers/` - Create new customer
- `GET /customers/` - List all customers (with pagination)
- `GET /customers/{id}` - Get customer by ID
- `PUT /customers/{id}` - Update customer (requires auth)
- `DELETE /customers/{id}` - Delete customer (requires auth)
- `POST /customers/login` - Customer authentication
- `GET /customers/my-tickets` - Get customer's service tickets (requires auth)

#### Mechanics (`/mechanics`)
- `POST /mechanics/` - Create new mechanic
- `GET /mechanics/` - List all mechanics
- `GET /mechanics/{id}` - Get mechanic by ID
- `PUT /mechanics/{id}` - Update mechanic
- `DELETE /mechanics/{id}` - Delete mechanic
- `GET /mechanics/most-active` - Get mechanics sorted by ticket count

#### Service Tickets (`/service_tickets`)
- `POST /service_tickets/` - Create new service ticket
- `GET /service_tickets/` - List all service tickets
- `PUT /service_tickets/{id}/assign-mechanic/{mechanic_id}` - Assign mechanic
- `PUT /service_tickets/{id}/remove-mechanic/{mechanic_id}` - Remove mechanic
- `PUT /service_tickets/{id}/edit` - Bulk add/remove mechanics
- `PUT /service_tickets/{id}/add-part/{part_id}` - Add inventory part

#### Inventory (`/inventory`)
- `POST /inventory/` - Create new inventory item
- `GET /inventory/` - List all inventory items
- `GET /inventory/{id}` - Get inventory item by ID
- `PUT /inventory/{id}` - Update inventory item
- `DELETE /inventory/{id}` - Delete inventory item

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Getting a Token
```bash
POST /customers/login
Content-Type: application/json

{
    "email": "customer@example.com",
    "password": "password123"
}
```

### Using the Token
Include the token in the Authorization header:
```bash
Authorization: Bearer <your-jwt-token>
```

### Protected Routes
Routes requiring authentication are marked with `@token_required` decorator:
- Customer update/delete operations
- Accessing personal service tickets (`/my-tickets`)

## Usage Examples

### Create a Customer
```bash
curl -X POST http://localhost:5000/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-123-4567",
    "password": "securepassword"
  }'
```

### Login and Get Token
```bash
curl -X POST http://localhost:5000/customers/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword"
  }'
```

### Create Service Ticket
```bash
curl -X POST http://localhost:5000/service_tickets/ \
  -H "Content-Type: application/json" \
  -d '{
    "VIN": "1234567890ABCDEFG",
    "service_date": "2024-01-15T10:00:00",
    "service_desc": "Oil change and tire rotation",
    "customer_id": 1
  }'
```

### Get Customer's Tickets (Authenticated)
```bash
curl -X GET http://localhost:5000/customers/my-tickets \
  -H "Authorization: Bearer <your-jwt-token>"
```

## Testing

The project includes comprehensive test coverage for all endpoints.

### Running Tests
```bash
# Run all tests from project root
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_customers

# Run with verbose output
python -m unittest discover tests -v
```

### Test Structure
- `test_customers.py` - Customer endpoint tests
- `test_mechanics.py` - Mechanic endpoint tests
- `test_service_tickets.py` - Service ticket tests
- `test_inventory.py` - Inventory management tests

### Test Coverage
- ✅ Positive test cases (valid operations)
- ✅ Negative test cases (invalid data, missing fields)
- ✅ Authentication and authorization
- ✅ Error handling
- ✅ Edge cases and boundary conditions

## Database Schema

### Core Models

#### Customer
- `id` - Primary key
- `name` - Customer name
- `email` - Unique email address
- `phone` - Contact number
- `password` - Hashed password

#### Mechanic
- `id` - Primary key
- `name` - Mechanic name
- `email` - Unique email address
- `phone` - Contact number
- `salary` - Mechanic salary

#### ServiceTicket
- `id` - Primary key
- `VIN` - Vehicle identification number
- `service_date` - Date of service
- `service_desc` - Description of service
- `customer_id` - Foreign key to Customer

#### Inventory
- `id` - Primary key
- `name` - Part name
- `price` - Part price

### Relationships
- **Customer ↔ ServiceTicket**: One-to-Many
- **ServiceTicket ↔ Mechanic**: Many-to-Many (via ServiceMechanic)
- **ServiceTicket ↔ Inventory**: Many-to-Many (via ServicePart)

## Rate Limiting & Caching

### Rate Limiting
- Customer creation: 6 requests per hour per IP
- Configurable limits using Flask-Limiter
- Prevents API abuse and ensures fair usage

### Caching
- Customer list endpoint cached for 60 seconds
- Improves response times for frequently accessed data
- Uses Flask-Caching with SimpleCache backend

## API Response Format

### Success Response
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-123-4567"
}
```

### Error Response
```json
{
  "error": "Email already exists"
}
```

### Validation Error Response
```json
{
  "email": ["Missing data for required field."],
  "password": ["Shorter than minimum length 6."]
}
```

## Development Guidelines

### Adding New Endpoints
1. Create route in appropriate blueprint
2. Add Marshmallow schema for validation
3. Include Swagger documentation
4. Write comprehensive tests
5. Update this README if needed

### Code Style
- Follow PEP 8 guidelines
- Use descriptive variable names
- Include docstrings for functions
- Validate all input data

### Security Considerations
- Always validate and sanitize input
- Use parameterized queries to prevent SQL injection
- Implement proper authentication for sensitive operations
- Keep JWT secret key secure

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please open an issue in the repository or contact the development team.

---

**Happy coding! 🔧⚙️**
