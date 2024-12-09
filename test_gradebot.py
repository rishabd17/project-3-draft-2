import pytest
from app import app, db, PrivateKey, encrypt_private_key, decrypt_private_key

from app import db

# Create all tables
with app.app_context():
    db.create_all()

# Fixture to create a test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test for storing and retrieving a private key
def test_private_key_storage(client):
    """
    Test if a private key is stored and retrieved correctly.
    """
    private_key = "testprivatekey"
    encrypted_key = encrypt_private_key(private_key)
    
    # Store in the database
    new_key = PrivateKey(name="test_private_key", encrypted_key=encrypted_key)
    with app.app_context():
        db.session.add(new_key)
        db.session.commit()

    # Retrieve from the database
    with app.app_context():
        stored_key = PrivateKey.query.filter_by(name="test_private_key").first()

    # Assert the private key is correctly stored and decrypted
    assert stored_key is not None
    assert stored_key.name == "test_private_key"
    decrypted_key = decrypt_private_key(stored_key.encrypted_key)
    assert decrypted_key == private_key

# Test for checking if app is running correctly
def test_home(client):
    """
    Test if the home route returns the correct response.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Flask Encryption App!" in response.data
