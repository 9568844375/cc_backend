# === utils/jwt_helper.py ===
from datetime import datetime, timedelta
from jose import jwt
from cc_config import SECRET_KEY, ALGORITHM

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
