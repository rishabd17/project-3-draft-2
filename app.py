from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import os

# Load environment variables from .env file
load_dotenv()

# Validate and load the encryption key from environment variables
AES_KEY = os.getenv('NOT_MY_KEY')
if not AES_KEY:
    raise ValueError("Encryption key (NOT_MY_KEY) is not set in the environment variables.")

# Initialize Fernet cipher
fernet = Fernet(AES_KEY)

# Flask application and database setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class PrivateKey(db.Model):
    __tablename__ = 'private_keys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    encrypted_key = db.Column(db.String(255), nullable=False)

# Encryption/Decryption Utility Functions
def encrypt_private_key(private_key: str) -> str:
    """
    Encrypts a private key using Fernet encryption.
    
    :param private_key: The plaintext private key to encrypt.
    :return: Encrypted private key as a string.
    """
    return fernet.encrypt(private_key.encode()).decode()

def decrypt_private_key(encrypted_private_key: str) -> str:
    """
    Decrypts an encrypted private key using Fernet decryption.
    
    :param encrypted_private_key: The encrypted private key to decrypt.
    :return: Decrypted private key as a string.
    """
    return fernet.decrypt(encrypted_private_key.encode()).decode()

# Database Initialization Function
def initialize_database():
    """
    Initializes the database by creating tables and adding default data.
    """
    with app.app_context():
        db.create_all()
        # Check if the private key already exists
        if not PrivateKey.query.filter_by(name="my_private_key").first():
            # Example: Encrypt and store a private key
            private_key = "mysecretprivatekey"
            encrypted_key = encrypt_private_key(private_key)
            new_key = PrivateKey(name="my_private_key", encrypted_key=encrypted_key)
            db.session.add(new_key)
            db.session.commit()
        else:
            print("Default private key already exists in the database.")

# Retrieve and Decrypt a Private Key
def retrieve_and_decrypt_key(name: str) -> str:
    """
    Retrieves and decrypts a private key from the database.
    
    :param name: The name of the private key to retrieve.
    :return: The decrypted private key.
    """
    with app.app_context():
        stored_key = PrivateKey.query.filter_by(name=name).first()
        if stored_key:
            return decrypt_private_key(stored_key.encrypted_key)
        raise ValueError(f"No private key found with name '{name}'")

# Flask Application Routes (Optional for APIs)
@app.route('/')
def home():
    return "Welcome to the Flask Encryption App!"

# Main Entry Point
if __name__ == "__main__":
    initialize_database()
    try:
        decrypted_key = retrieve_and_decrypt_key("my_private_key")
        print(f"Decrypted Private Key: {decrypted_key}")
    except ValueError as e:
        print(e)
    app.run(debug=True)

# Debugging environment variables
print("NOT_MY_KEY from .env:", os.getenv('NOT_MY_KEY'))
