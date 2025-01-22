from flask import Flask, request, jsonify, session
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# Decorator to protect routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # Get token from header
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token.split(' ')[1]

            # Decode the token
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user = decoded['user']  # Attach user info to the request
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 403

        return f(*args, **kwargs)

    return decorated


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()  # Get JSON data from the request
    email = data.get('email')
    password = data.get('password')

    if email == 'test@test.com' and password == '123456':  # Simple validation for demonstration
        token = jwt.encode({
            'user': email,
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)  # Token expires in 1 hour
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/api/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({'message': f'Welcome, {request.user}!'}), 200


if __name__ == '__main__':
    app.run(debug=True)
