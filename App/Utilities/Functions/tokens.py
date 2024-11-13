import bcrypt
import jwt
from uuid import uuid4

def encrypt_password(password: str) -> str:
    """
    Encrypts a password using bcrypt.

    Args:
        password (str): The password to be encrypted.

    Returns:
        str: The encrypted password.

    Raises:
        ValueError: If the password is empty or None.
        Exception: If there is an error during the encryption process.
    """
    if not password:
        raise ValueError("Password cannot be empty or None.")

    try:
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()
    except Exception as e:
        raise Exception("Error encrypting password: " + str(e))

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed password using bcrypt.

    Args:
        password (str): The password to be verified.
        hashed_password (str): The hashed password to be compared against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.

    Raises:
        ValueError: If the password or hashed password is empty or None.
        Exception: If there is an error during the verification process.
    """
    if not password:
        raise ValueError("Password cannot be empty or None.")
    if not hashed_password:
        raise ValueError("Hashed password cannot be empty or None.")

    try:
        return bcrypt.checkpw(password.encode('utf8'), hashed_password)
    except Exception as e:
        raise Exception("Error verifying password: " + str(e))

def generate_jwt(payload: dict, secret_key: str, algorithm: str = "HS256") -> str:
    """
    Generates a JSON Web Token (JWT) using the provided payload and secret key.

    Args:
        payload (dict): The payload to be included in the JWT.
        secret_key (str): The secret key used to sign the JWT.
        algorithm (str, optional): The algorithm used for signing the JWT. Defaults to "HS256".

    Returns:
        str: The generated JWT.

    Raises:
        ValueError: If the payload or secret key is empty or None.
        Exception: If there is an error during the JWT generation process.
    """
    if not payload:
        raise ValueError("Payload cannot be empty or None.")
    if not secret_key:
        raise ValueError("Secret key cannot be empty or None.")

    try:
        encoded_jwt = jwt.encode(payload, secret_key, algorithm=algorithm)
        return encoded_jwt
    except Exception as e:
        raise Exception("Error generating JWT: " + str(e))
    
def decode_jwt(token: str, secret_key: str, algorithm: str = "HS256") -> dict:
    """
    Decodes a JSON Web Token (JWT) using the provided token and secret key.

    Args:
        token (str): The JWT to be decoded.
        secret_key (str): The secret key used to sign the JWT.
        algorithm (str, optional): The algorithm used for signing the JWT. Defaults to "HS256".

    Returns:
        dict: The decoded payload of the JWT.

    Raises:
        ValueError: If the token or secret key is empty or None.
        Exception: If there is an error during the JWT decoding process.
    """
    if not token:
        raise ValueError("Token cannot be empty or None.")
    if not secret_key:
        raise ValueError("Secret key cannot be empty or None.")

    try:
        decoded_jwt = jwt.decode(token, secret_key, algorithms=[algorithm])
        return decoded_jwt
    except Exception as e:
        raise Exception("Error decoding JWT: " + str(e))

def verify_jwt(token: str, secret_key: str, algorithm: str = "HS256") -> bool:
    """
    Verifies a JSON Web Token (JWT) using the provided token and secret key.

    Args:
        token (str): The JWT to be verified.
        secret_key (str): The secret key used to sign the JWT.
        algorithm (str, optional): The algorithm used for signing the JWT. Defaults to "HS256".

    Returns:
        bool: True if the JWT is valid, False otherwise.

    Raises:
        ValueError: If the token or secret key is empty or None.
        Exception: If there is an error during the JWT verification process.
    """
    if not token:
        raise ValueError("Token cannot be empty or None.")
    if not secret_key:
        raise ValueError("Secret key cannot be empty or None.")

    try:
        jwt.decode(token, secret_key, algorithms=[algorithm])
        return True
    except Exception as e:
        return False
    
def generate_token () :
    """
    Generate a random token.

    Returns:
        str: The generated token.
    """
    return str(uuid4())
