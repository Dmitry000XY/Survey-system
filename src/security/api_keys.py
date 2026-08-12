import hashlib
import hmac


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
