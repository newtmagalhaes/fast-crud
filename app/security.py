from pydantic import SecretStr


def hash_password(password: SecretStr) -> str:
    # TODO: resolve hashing
    return password.get_secret_value()
