from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "your_secret_key"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Look for the token in the Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            customer_id = int(data['sub'])  # Ensure it's an int if your DB uses int PKs
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Invalid token!'}), 401

        # Pass customer_id to the wrapped function
        return f(*args, customer_id_from_token=customer_id, **kwargs)

    return decorated

def encode_token(customer_id):
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        "iat": datetime.now(timezone.utc),
        "sub": str(customer_id)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

