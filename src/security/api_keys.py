import hashlib
import hmac


def hash_api_key(api_key: str) -> str:
    """Return the irreversible SHA-256 fingerprint stored for an API key."""

    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def verify_api_key(api_key: str, expected_hash: str) -> bool:
    """Compare an API key with a stored fingerprint in constant time."""

    return hmac.compare_digest(hash_api_key(api_key), expected_hash)
