import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import logging
from typing import Optional

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def get_encryption_key() -> bytes:
    """Get or generate the encryption key using environment variables."""
    key = os.getenv("SLACK_ENCRYPTION_KEY")
    logger.debug(f"SLACK_ENCRYPTION_PASSWORD exists: {bool(os.getenv('SLACK_ENCRYPTION_PASSWORD'))}")
    logger.debug(f"SLACK_ENCRYPTION_SALT exists: {bool(os.getenv('SLACK_ENCRYPTION_SALT'))}")
    
    if not key:
        # Generate a new key if none exists
        salt = os.getenv("SLACK_ENCRYPTION_SALT", "nia_salt").encode()
        password = os.getenv("SLACK_ENCRYPTION_PASSWORD")
        if not password:
            logger.error("SLACK_ENCRYPTION_PASSWORD not found in environment")
            raise ValueError("SLACK_ENCRYPTION_PASSWORD must be set")
            
        # Use PBKDF2 to derive a key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        
    return key if isinstance(key, bytes) else key.encode()

def get_cipher() -> Fernet:
    """Get the Fernet cipher instance using our encryption key."""
    try:
        key = get_encryption_key()
        return Fernet(key)
    except Exception as e:
        logger.error(f"Failed to initialize cipher: {e}")
        raise

def encrypt_token(token: str) -> Optional[str]:
    """Encrypt a token string."""
    if not token:
        return None
        
    try:
        cipher = get_cipher()
        encrypted = cipher.encrypt(token.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    except Exception as e:
        logger.error(f"Failed to encrypt token: {e}")
        return None

def decrypt_token(encrypted_token: str) -> Optional[str]:
    """Decrypt an encrypted token string."""
    if not encrypted_token:
        return None
        
    try:
        cipher = get_cipher()
        decoded = base64.urlsafe_b64decode(encrypted_token.encode())
        decrypted = cipher.decrypt(decoded)
        return decrypted.decode()
    except Exception as e:
        logger.error(f"Failed to decrypt token: {e}")
        return None 