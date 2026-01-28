import bcrypt


def is_valid_password(password: str, pass_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), pass_hash.encode("utf-8"))


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(
        salt=bcrypt.gensalt(), password=password.encode("utf-8")
    ).decode("utf-8")
