from src.configurations.constants import API_KEY_LENGTH, generate_api_key
from src.security import hash_api_key, verify_api_key


def test_api_key_is_returned_plain_and_stored_as_sha256_hash() -> None:
    api_key = generate_api_key()
    api_key_hash = hash_api_key(api_key)

    assert len(api_key) == API_KEY_LENGTH
    assert len(api_key_hash) == 64
    assert api_key != api_key_hash
    assert verify_api_key(api_key, api_key_hash)
    assert not verify_api_key(f"{api_key}x", api_key_hash)
