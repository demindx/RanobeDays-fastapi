from datetime import UTC, datetime, timedelta

import jwt

from src.auth.exceptions import TokenError
from src.auth.schemas import TokenData
from src.config import config


def generate_jwt_token(user_id: int, delta: timedelta = timedelta(minutes=30)) -> str:
    now = datetime.now(UTC)
    exp_time = now + delta
    exp_timestamp = int(exp_time.timestamp())

    payload = {"sub": str(user_id), "exp": exp_timestamp}

    return jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")


def decode_jwt_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise TokenError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise TokenError(f"Invalid token: {e}")
    except Exception as e:
        raise TokenError(f"Token validation failed: {e}")

    payload["exp"] = datetime.fromtimestamp(payload["exp"], UTC)

    return TokenData(**payload)
