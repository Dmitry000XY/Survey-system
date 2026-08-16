import hashlib
import hmac
import secrets

from src.configurations.constants import API_KEY_ENTROPY_BYTES, API_KEY_LENGTH


def generate_api_key() -> str:
    """Generate a high-entropy API key that is shown to the client only once."""

    api_key = secrets.token_urlsafe(API_KEY_ENTROPY_BYTES)
    if len(api_key) != API_KEY_LENGTH:
        raise RuntimeError("Generated API key has an unexpected length")
    return api_key


def hash_api_key(api_key: str) -> str:
    """Return the irreversible fingerprint stored for a generated API key.

    API keys contain 384 bits of cryptographic randomness, so a fast hash is
    appropriate here. Passwords are lower-entropy secrets and must never use
    this function; they require a dedicated, computationally expensive KDF.
    """

    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def verify_api_key(api_key: str, expected_hash: str) -> bool:
    """Compare an API key with a stored fingerprint in constant time."""

    return hmac.compare_digest(hash_api_key(api_key), expected_hash)
