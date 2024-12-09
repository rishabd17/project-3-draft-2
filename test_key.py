from cryptography.fernet import Fernet


key = "jXLj6bvG0vPBjHdBCcxFcPS-TstcDuD6aapjnW2WOL8="

try:
    # Initialize Fernet with the provided key
    fernet = Fernet(key)
    print("Key is valid and Fernet is initialized!")
except Exception as e:
    print("Invalid Fernet key:", e)

