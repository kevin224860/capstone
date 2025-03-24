from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import re

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
        cur.execute("SELECT s.entry_ID, s.stock, i.name, s.number, s.price_per_share, s.date FROM StockEntry s INNER JOIN Industry i ON s.industry_ID = i.industry_ID WHERE user_ID = %s ORDER BY entry_ID", (user_id,))
        columns = ["entry_ID", "stock", "name", "number", "price_per_share", "date"]
        stocks = [dict(zip(columns, row)) for row in cur.fetchall()]
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
@app.route("/api/suggestions", methods=["GET"])
@jwt_required()
def get_suggestions():
    user_email = get_jwt_identity()
    
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get user ID
        cur.execute("SELECT user_id FROM AccountUser WHERE email = %s", (user_email,))
        user = cur.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        user_id = user['user_id']

        # Get all industries with minimum count
        cur.execute("""
            WITH industry_counts AS (
                SELECT i.industry_id, COUNT(*)::INT
                FROM StockEntry s
                JOIN Industry i ON s.industry_id = i.industry_id
                WHERE user_id = %s
                GROUP BY i.industry_id
            )
            SELECT industry_id
            FROM industry_counts
            WHERE count = (SELECT MIN(count) FROM industry_counts)
        """, (user_id,))
        
        min_industries = [row['industry_id'] for row in cur.fetchall()]

        # Get suggestions from all minimum industries
        cur.execute("""
            SELECT sp.ticker_symbol AS ticker,
                   sp.name AS name,
                   i.name AS industry,
                   ai.rating AS rating
            FROM AISuggestions ai
            JOIN StockPool sp ON ai.stock_id = sp.stock_id
            JOIN Industry i ON ai.industry_id = i.industry_id
            WHERE ai.industry_id = ANY(%s)
            AND sp.ticker_symbol NOT IN (
                SELECT stock FROM StockEntry WHERE user_id = %s
            )
            ORDER BY ai.rating DESC
            LIMIT 3
        """, (min_industries, user_id))
        
        suggestions = cur.fetchall()

        # If less than 3 suggestions, fill with other industries
        if len(suggestions) < 3:
            cur.execute("""
                SELECT sp.ticker_symbol AS ticker,
                       sp.name AS name,
                       i.name AS industry,
                       ai.rating AS rating
                FROM AISuggestions ai
                JOIN StockPool sp ON ai.stock_id = sp.stock_id
                JOIN Industry i ON ai.industry_id = i.industry_id
                WHERE sp.ticker_symbol NOT IN (
                    SELECT stock FROM StockEntry WHERE user_id = %s
                )
                ORDER BY ai.rating DESC
                LIMIT %s
            """, (user_id, 3 - len(suggestions)))
            suggestions += cur.fetchall()

        # Convert ratings
        for suggestion in suggestions:
            rating = suggestion['rating']
            suggestion['confidence'] = int((rating / 5) * 100)
            suggestion['rating'] = "Strong Buy" if rating >= 4.5 else "Buy" if rating >= 4.0 else "Hold"

        return jsonify({'suggestions': suggestions[:3]}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
@app.route("/api/industries", methods=["GET"])
def get_industries():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * from Industry;")
    industries = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify({
            'industries': industries,
            'status': 'success'
        })

@app.route('/api/addstock', methods=['POST'])
@jwt_required()
def add_stock():
    data = request.get_json()
    user_email = get_jwt_identity()
    symbol = data['stock']
    industry = data['industry_id']
    try:
        number = int(data['number'])  # Convert to integer
    except ValueError:
        return jsonify({"error": "Number must be a positive integer"}), 400
    
    price_per_share = data['price_per_share']
    date = data['date']

    print("Received data:", data) 

    if not all([symbol, industry, number, price_per_share, date]):
        return jsonify({"error": "All fields (symbol, industry, number, price_per_share, date) are required"}), 400

    symbol_regex=r'^[A-Z0-9]{1,5}([.\-][A-Z0-9]{1,3})?$'
    if not re.match(symbol_regex, symbol):
        return jsonify({"error": "Invalid stock ticker symbol"}), 400 

    numprice_pattern = r'^\d+(\.\d{1,2})?$'
    if not isinstance(price_per_share, (int, float)) or price_per_share <= 0:
        return jsonify({"error": "Invalid price per share"}), 400 

    if not isinstance(number, int) or number <= 0:
        return jsonify({"error": "Number must be a positive integer"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT user_ID FROM AccountUser WHERE email = %s", (user_email,))
        doesExist = cur.fetchone()
        print(doesExist[0])
        # cannot have an account with the same email address
        if not doesExist:
            return jsonify({"error": "An error occured"}), 400

        cur.execute(
            "INSERT INTO StockEntry (user_ID, Industry_ID, stock, number, date, price_per_share) VALUES (%s, %s, %s, %s, %s, %s) RETURNING entry_ID",
            (doesExist[0], industry, symbol, number, date, price_per_share)
        )
        stock_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "User registered successfully", "stock_id": stock_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route("/api/portfolio/<int:entry_id>", methods=["DELETE"])
@jwt_required()
def delete_stock(entry_id):
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
        
        cur.execute("SELECT entry_ID FROM StockEntry WHERE entry_ID = %s AND user_ID = %s", (entry_id, user_id))
        stock_entry = cur.fetchone()

        if not stock_entry:
            return jsonify({"error": "Stock not found"}), 404

        cur.execute(
            "DELETE FROM StockEntry WHERE entry_ID = %s AND user_ID = %s",
            (entry_id, user_id)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "User deleted stock successfully", "entry_id": entry_id}), 200

    except Exception as e:
        print(f"🔥 Error deleting stock: {str(e)}")

        return jsonify({"error": str(e)}), 500

@app.route("/api/portfolio/edit/<int:entry_id>", methods=["PUT"])
@jwt_required()
def update_stock(entry_id):
    data = request.get_json()
    user_email = get_jwt_identity()
    symbol = data['stock']
    industry = data['name']
    try:
        number = int(data['number'])  # Convert to integer
    except ValueError:
        return jsonify({"error": "Number must be a positive integer"}), 400
    
    price_per_share = data['price_per_share']
    date = data['date']
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if user exists
        cur.execute("SELECT user_ID FROM AccountUser WHERE email = %s", (user_email,))
        user = cur.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id = user[0]  # Extract the user_ID
        
        cur.execute("SELECT entry_ID FROM StockEntry WHERE entry_ID = %s AND user_ID = %s", (entry_id, user_id))
        stock_entry = cur.fetchone()

        if not stock_entry:
            return jsonify({"error": "Stock not found"}), 404

        cur.execute(
            "UPDATE StockEntry SET entry_ID = %s, industry_id = %s, stock = %s, number = %s, price_per_share = %s, date = %s WHERE entry_ID = %s AND user_ID = %s",
            (entry_id, industry, symbol, number, price_per_share, date, entry_id, user_id)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Stock updated successfully", "entry_id": entry_id}), 200

    except Exception as e:
        print(f"🔥 Error updating stock: {str(e)}")

        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
