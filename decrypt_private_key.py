from cryptography.fernet import Fernet

def decrypt_private_key(encrypted_key):
    """Decrypt the encrypted private key."""
    key = b"jXLj6bvG0vPBjHdBCcxFcPS-TstcDuD6aapjnW2WOL8="  
    fernet = Fernet(key)
    decrypted_key = fernet.decrypt(encrypted_key.encode()).decode()
    return decrypted_key
