from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password: str) -> bytes:
    """Derive a secure key from the password."""
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_file(file_path: str, password: str):
    print(f"Encrypting: {file_path}")

    key = generate_key(password)
    fernet = Fernet(key)
    
    with open(file_path, 'rb') as file:
        original = file.read()
    
    encrypted = fernet.encrypt(original)
    
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    
    print(f"Encrypted {file_path}")

def decrypt_file(file_path: str, password: str):
    key = generate_key(password)
    fernet = Fernet(key)
    
    with open(file_path, 'rb') as enc_file:
        encrypted = enc_file.read()
    
    decrypted = fernet.decrypt(encrypted)
    
    with open(file_path, 'wb') as dec_file:
        dec_file.write(decrypted)
    
    print(f"Decrypted {file_path}")
