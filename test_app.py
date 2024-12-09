import pytest
from app import app, db, PrivateKey, encrypt_private_key, decrypt_private_key

@pytest.fixture(scope="module")
def setup_database():
    """Set up the database before tests run."""
    with app.app_context():
        db.create_all()  # Create tables
    yield
    with app.app_context():
        db.drop_all()  # Clean up after tests run

@pytest.fixture
def clear_private_keys():
    """Clear the private_keys table before each test to avoid conflicts."""
    with app.app_context():
        db.session.query(PrivateKey).delete()  # Clear the table
        db.session.commit()

def test_private_key_storage(clear_private_keys):
    """Test if a private key is stored and retrieved correctly."""
    private_key = "testprivatekey"
    encrypted_key = encrypt_private_key(private_key)
    
    # Use a unique name for each test
    unique_name = "test_private_key_1"  # Change this to a unique name for each test

    # Store in the database
    with app.app_context():
        new_key = PrivateKey(name=unique_name, encrypted_key=encrypted_key)
        db.session.add(new_key)
        db.session.commit()

    # Assert that the key has been stored
    with app.app_context():
        stored_key = PrivateKey.query.filter_by(name=unique_name).first()
        assert stored_key is not None
        assert stored_key.name == unique_name
        assert stored_key.encrypted_key == encrypted_key

def test_private_key_retrieval(clear_private_keys):
    """Test if the encrypted private key is retrievable and decrypts correctly."""
    # Store a new key
    private_key = "anotherprivatekey"
    encrypted_key = encrypt_private_key(private_key)
    unique_name = "test_private_key_2"  # Unique name for this test

    with app.app_context():
        new_key = PrivateKey(name=unique_name, encrypted_key=encrypted_key)
        db.session.add(new_key)
        db.session.commit()

    # Retrieve the private key from the database
    with app.app_context():
        stored_key = PrivateKey.query.filter_by(name=unique_name).first()
        decrypted_key = decrypt_private_key(stored_key.encrypted_key)

    # Assert that the decrypted key matches the original key
    assert decrypted_key == "anotherprivatekey"
