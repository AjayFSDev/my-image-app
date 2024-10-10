from flask import Flask, request, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import os
import psycopg2
from flask_cors import CORS
from flask import Flask, jsonify

app = Flask(__name__, static_url_path='/assets', static_folder='C:/Users/ajaya/Documents/my-image-app/src/assets')
CORS(app)  # Enable CORS
UPLOAD_FOLDER = 'C:/Users/ajaya/Documents/my-image-app/src/assets'
def list_images():
    try:
        images = [f'/assets/{filename}' for filename in os.listdir(UPLOAD_FOLDER) if filename.endswith(('png', 'jpg', 'jpeg', 'gif'))]
        return jsonify(images)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PostgreSQL connection parameters
DB_HOST = 'localhost'
DB_NAME = 'my_image_app_db'
DB_USER = 'postgres'  # Your PostgreSQL username
DB_PASS = 'ammaappasis'  # Your PostgreSQL password

# Local directory to store uploaded images
UPLOAD_FOLDER = app.static_folder

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

# User registration endpoint
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone() is not None:
            return jsonify({"error": "Username already exists."}), 400

        # Insert new user
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user is None or not check_password_hash(user[0], password):
            return jsonify({"error": "Invalid username or password."}), 401

        return jsonify({"message": "Login successful!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Upload endpoint
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save file to local directory
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)  # Save the file to the specified directory
        
        # Store metadata in PostgreSQL
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO images (filename, url) VALUES (%s, %s)',
            (file.filename, f'/assets/{file.filename}')  # Save the relative path to the database
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'File uploaded successfully', 'url': f'/assets/{file.filename}'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to serve the uploaded files
@app.route('/assets/<path:filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Endpoint to fetch all uploaded images
@app.route('/images', methods=['GET'])
def list_images():
    try:
        # List all files in the UPLOAD_FOLDER
        files = os.listdir(UPLOAD_FOLDER)
        # Filter for image files (you can add more formats if needed)
        images = [{'url': f'/assets/{file}'} for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        return jsonify(images), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

