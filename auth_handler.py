from datetime import datetime, timedelta
import jwt, os

from datetime import timezone
SECRET_KEY = os.getenv("JWT_SECRET")

def decodeJWT(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

def create_jwt_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")