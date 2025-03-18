from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

# Load environment variables
load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)

# CORS allows the frontend
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY",
                                         "your_secret_key")  # add in your secret key in for the encryption
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)  # jwt token expires in 30 minutes
app.config["JWT_TOKEN_LOCATION"] = ["headers"]  # jwt token is in the header

jwt = JWTManager(app)


# connect to the PostgreSQL database
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('HOST'),
        port=os.getenv('PORT'),
        database=os.getenv('DATABASE'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD')
    )


# API to responsible for the signup of users
@app.route('/api/signup', methods=['POST'])
def signup():
    # get all the values of the text fields from the frontend
    data = request.get_json()
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    password = data['password']

    # make sure that all fields are filled out
    if not all([first_name, last_name, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    # hash password because the database stores a one way encrypted password for security
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # connect to the database
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT email FROM AccountUser WHERE email = %s", (email,))
        doesExist = cur.fetchone()

        # cannot have an account with the same email address
        if doesExist:
            return jsonify({"error": "An account already exists with that email"}), 400

        cur.execute(
            "INSERT INTO AccountUser (first_name, last_name, email, password) VALUES (%s, %s, %s, %s) RETURNING id",
            (first_name, last_name, email, hashed_password)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API used to log in to an account
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Check if email exists
        cur.execute("SELECT user_ID, password FROM AccountUser WHERE email = %s", (email,))
        user = cur.fetchone()

        if not user:
            return jsonify({"message": "Invalid credentials"}), 401

        print(f"User found: {user}")

        # Validate password
        if not bcrypt.check_password_hash(user["password"], password):
            print("Password does not match")
            return jsonify({"message": "Invalid credentials"}), 401

        # Generate JWT token
        token = create_access_token(identity=email)
        print("Login successful, token generated")

        return jsonify({"token": token}), 200

    except Exception as e:
        print("Error:", str(e))  # Print the actual error to Flask logs
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=["GET"])
def index():
    return jsonify({"status":"ok"}), 200

# API to get all the info for the users dashboard
@app.route("/api/dashboard", methods=["GET"])
@jwt_required()
def get_dashboard():
    # gets the identity of the user from jwt
    user_email = get_jwt_identity()

    # connect to database
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # query to get info from the db
        cur.execute("SELECT user_id, first_name FROM AccountUser WHERE email = %s", (user_email,))
        user = cur.fetchone()

        if not user:
            cur.close()
            conn.close()
            return jsonify({"message": "User not found"}), 404

        first_name = user["first_name"]

        cur.close()
        conn.close()

        return jsonify({
            "first_name": first_name
        }), 200
    except Exception as e:
        print("Error in /api/dashboard:", str(e))
        return jsonify({"error": str(e)}), 500


# portfolio API requires JWT Auth
@app.route("/api/portfolio", methods=["GET"])
@jwt_required()
def get_portfolio():
    # Get the user's email from JWT
    user_email = get_jwt_identity()

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if user exists
        cur.execute("SELECT user_ID FROM AccountUser WHERE email = %s", (user_email,))
        user = cur.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id = user[0]  # Extract the user_ID

        # Get stock entries for this user
        cur.execute("SELECT s.stock, i.name, s.number, s.price_per_share, s.date FROM StockEntry s INNER JOIN Industry i ON s.industry_ID = i.industry_ID WHERE user_ID = %s", (user_id,))
        stocks = cur.fetchall()
        cur.close()
        conn.close()
        print(stocks)
        return jsonify({
            'portfolio': stocks,
            'status': 'success'
        })

    except Exception as e:
        print(f"🔥 Error in /api/portfolio: {str(e)}")  # Log error
        return jsonify({"error": str(e)}), 500





if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
