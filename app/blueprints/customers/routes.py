from .schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, ServiceTicket
from . import customers_bp
from app.blueprints.customers import customers_bp
from app.extensions import limiter, cache, db
from app.utils.util import encode_token, token_required
from flasgger import swag_from 

#Endpoints
#Create new customer
@customers_bp.route('/', methods=['POST'])  
@limiter.limit("6 per hour")
def add_customer():
    """
    Create a new customer
    ---
    tags:
      - Customers
    summary: Create a new customer
    description: Creates a new customer account with the provided information
    parameters:
      - in: body
        name: customer
        description: Customer information
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - phone
            - password
          properties:
            name:
              type: string
              example: "John Doe"
            email:
              type: string
              format: email
              example: "johndoe@email.com"
            phone:
              type: string
              example: "555-123-4567"
            password:
              type: string
              example: "securepassword123"
    responses:
      201:
        description: Customer created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "John Doe"
            email:
              type: string
              example: "johndoe@email.com"
            phone:
              type: string
              example: "555-123-4567"
      400:
        description: Bad request - validation error or email already exists
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Email already exists"
    """
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == customer_data['email']) 
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"error": "Email already exists"}), 400

    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

#Read all customers
@customers_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    start = (page - 1) * per_page
    end = start + per_page
    paginated = customers[start:end]
    return customers_schema.jsonify(paginated)

#Read a specific customer by ID
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"message": "Customer not found"}), 404

# Update customer by ID
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@token_required
def update_customer(customer_id, customer_id_from_token):
    if customer_id != customer_id_from_token:
        return jsonify({"error": "Unauthorized"}), 403

    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    try:
        customer_data = customer_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200

# Delete a customer by ID
@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@token_required
def delete_customer_by_id(customer_id, customer_id_from_token):
    """
    Given a customer ID, this endpoint will delete the customer from the database.
    The deletion is only allowed if the customer ID in the URL matches the customer ID
    associated with the JWT token provided in the Authorization header.
    If the two IDs do not match, a 403 Forbidden response is returned.
    If the customer is not found in the database, a 404 Not Found response is returned.
    If the deletion is successful, a 200 OK response is returned with a JSON message
    indicating that the customer was deleted successfully.
    """
    if customer_id != customer_id_from_token:
        # If the IDs don't match, we have an unauthorized request
        return jsonify({"error": "Unauthorized"}), 403

    customer = db.session.get(Customer, customer_id)
    if not customer:
        # If the customer can't be found in the database, return a 404
        return jsonify({"error": "Customer not found"}), 404

    # Delete the customer from the database
    db.session.delete(customer)
    db.session.commit()
    # Return a 200 OK response with a JSON message indicating success
    return jsonify({"message": "Customer deleted successfully"}), 200

#Login customer
@customers_bp.route('/login', methods=['POST'])
def login():
    """
    Customer login
    ---
    tags:
      - Customers
    summary: Authenticate customer
    description: Login with email and password to receive authentication token
    parameters:
      - in: body
        name: credentials
        description: Login credentials
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              format: email
              example: "johndoe@email.com"
            password:
              type: string
              example: "securepassword123"
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Login successful"
            auth_token:
              type: string
              example: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
      401:
        description: Invalid credentials
        schema:
          type: object
          properties:
            messages:
              type: string
              example: "Invalid username or password"
    """
    try:
        credentials = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    username = credentials['email']
    password = credentials['password']

    query = select(Customer).where(Customer.email == username)
    customer = db.session.execute(query).scalar_one_or_none()

    #if we have a customer associated with the username, validate the password
    if customer and customer.password == password: 
        auth_token = encode_token(customer.id)

        response = {
            "status": "success",
            "message": "Login successful",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({"messages": "Invalid username or password"}), 401

# Get all service tickets for a customer
@customers_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id_from_token):
    """
    Get customer's service tickets
    ---
    tags:
      - Customers
    summary: Get all service tickets for authenticated customer
    description: Returns all service tickets associated with the authenticated customer
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of customer's service tickets
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              VIN:
                type: string
                example: "1234567890ABCDEFG"
              service_date:
                type: string
                format: date-time
                example: "2024-01-15T10:00:00"
              service_desc:
                type: string
                example: "Oil change and tire rotation"
              customer_id:
                type: integer
                example: 1
      401:
        description: Unauthorized - Invalid or missing token
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Token is missing!"
    """
    # Query all service tickets for this customer
    query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id_from_token)
    tickets = db.session.execute(query).scalars().all()
    from app.blueprints.service_tickets.schemas import service_tickets_schema
    return service_tickets_schema.jsonify(tickets), 200

