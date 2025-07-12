# Mechanic Shop API 🚀

A comprehensive Flask-based REST API for managing a mechanic shop's operations, including customer management, service tickets, mechanic assignments, and inventory tracking. **Now live in production!**

## 🌐 Live Demo
**Production API**: `https://your-app-name.onrender.com`  
**Swagger Documentation**: `https://your-app-name.onrender.com/api/docs/`

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Live Demo & Deployment](#live-demo--deployment)
- [Project Structure](#project-structure)
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Database Schema](#database-schema)
- [Rate Limiting & Caching](#rate-limiting--caching)
- [Contributing](#contributing)

## Overview

The Mechanic Shop API is designed to streamline operations for automotive service businesses. It provides a complete backend solution for managing customers, mechanics, service tickets, and inventory with secure authentication, rate limiting, and comprehensive documentation.

**🎉 This API is production-ready and deployed on Render with a PostgreSQL database!**

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
- **Production Security**: Environment variables for sensitive data
- **PostgreSQL Database**: Reliable, hosted database solution

### Production Features
- **🚀 Deployed on Render**: Live production environment
- **🗄️ PostgreSQL Database**: Hosted database with reliable connections
- **🔐 Environment Variables**: Secure configuration management
- **📈 Gunicorn WSGI**: Production-grade web server
- **🌐 Custom Domain Ready**: Easily configurable for custom domains

### Advanced Features
- **Many-to-Many Relationships**: Complex relationships between tickets, mechanics, and parts
- **Pagination**: Efficient data retrieval for large datasets
- **Advanced Queries**: Analytics like most active mechanics
- **Swagger Documentation**: Interactive API documentation
- **Comprehensive Testing**: Full test coverage with positive and negative test cases

## 🌐 Live Demo & Deployment

### Production Environment
- **API Base URL**: `https://your-app-name.onrender.com`
- **Swagger UI**: `https://your-app-name.onrender.com/api/docs/`
- **Database**: PostgreSQL (hosted on Render)
- **Web Server**: Gunicorn WSGI
- **Platform**: Render.com

### Quick Test
Try the API immediately:
```bash
# Get all customers
curl https://your-app-name.onrender.com/customers/

# Health check (root endpoint)
curl https://your-app-name.onrender.com/
```

### Deployment Status
- ✅ **Live & Operational**
- ✅ **Database Connected**
- ✅ **Authentication Working**
- ✅ **Swagger Documentation Available**
- ✅ **Rate Limiting Active**

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
├── .env                           # Environment variables (local only)
├── .gitignore                     # Git ignore rules
├── config.py                      # Configuration settings
├── flask_app.py                   # Production entry point
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Local Development

### Prerequisites
- Python 3.8+
- Git
- Virtual environment support

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Mechanic-Shop-Flask-SQLAlchemy-DB.git
   cd Mechanic-Shop-Flask-SQLAlchemy-DB
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

4. **Set up environment variables**
   ```bash
   # Create .env file (copy from .env.example if available)
   SQLALCHEMY_DATABASE_URI=sqlite:///local.db  # For local development
   SECRET_KEY=your-local-secret-key
   ```

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
   python flask_app.py
   ```

   Access the local API at: `http://localhost:5000`
   Swagger docs at: `http://localhost:5000/api/docs/`

## Production Deployment

### Render Deployment (Current)

1. **Database Setup**
   - Create PostgreSQL database on Render
   - Note the external database URL

2. **Environment Variables**
   Set these in Render's environment settings:
   ```
   SQLALCHEMY_DATABASE_URI=postgresql://username:password@host:port/database
   SECRET_KEY=your-production-secret-key
   ```

3. **Deployment Configuration**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn flask_app:app`
   - **Python Version**: 3.13.4 (auto-detected)

4. **Deploy**
   - Connect GitHub repository to Render
   - Enable auto-deploy on pushes to main branch
   - Monitor deployment logs for any issues

### Alternative Deployment Options
- **Heroku**: Compatible with minor configuration changes
- **DigitalOcean App Platform**: Supported
- **AWS Elastic Beanstalk**: Can be configured
- **Google Cloud Run**: Container deployment ready

## Configuration

The application supports multiple environments configured in `config.py`:

- **DevelopmentConfig**: Local MySQL/SQLite database, debug mode enabled
- **TestingConfig**: SQLite database for isolated testing
- **ProductionConfig**: PostgreSQL database, production-ready settings

### Production Environment Variables
These are configured in your hosting platform (Render):
```bash
SQLALCHEMY_DATABASE_URI=postgresql://username:password@host:port/database
SECRET_KEY=your-secure-secret-key-here
```

### Local Development Environment Variables
Create a `.env` file for local development:
```bash
SQLALCHEMY_DATABASE_URI=sqlite:///local.db
SECRET_KEY=your-local-development-key
```

## API Documentation

### Interactive Documentation
Access the Swagger UI documentation at:
- **Production**: `https://your-app-name.onrender.com/api/docs/`
- **Local Development**: `http://localhost:5000/api/docs/`

### Base URLs
- **Production**: `https://your-app-name.onrender.com`
- **Local Development**: `http://localhost:5000`

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
# Production
curl -X POST https://your-app-name.onrender.com/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-123-4567",
    "password": "securepassword"
  }'

# Local Development
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
# Production
curl -X POST https://your-app-name.onrender.com/customers/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword"
  }'

# Local Development  
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

## 🎯 Production Checklist

This API is production-ready with the following implemented:

### ✅ Security
- [x] JWT Authentication
- [x] Environment variables for secrets
- [x] Input validation and sanitization
- [x] Rate limiting protection
- [x] CORS configuration

### ✅ Performance
- [x] Database connection pooling
- [x] Caching implementation
- [x] Gunicorn WSGI server
- [x] PostgreSQL database
- [x] Optimized queries

### ✅ Reliability
- [x] Comprehensive error handling
- [x] Database migrations support
- [x] Health check endpoints
- [x] Logging configuration
- [x] Production configuration

### ✅ Documentation & Testing
- [x] Swagger/OpenAPI documentation
- [x] Comprehensive test suite
- [x] README documentation
- [x] API examples and usage
- [x] Deployment instructions

### ✅ DevOps
- [x] Git version control
- [x] Render deployment
- [x] Environment management
- [x] Dependency management
- [x] CI/CD ready

---

**🚀 Ready for Production Use!**

This API is fully deployed, tested, and ready for real-world usage. All endpoints are functional, secure, and well-documented.

**Happy coding! 🔧⚙️**
