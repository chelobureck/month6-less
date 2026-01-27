import base64
from datetime import datetime, timezone, timedelta
from jwt import JWT, jwk_from_dict
from jwt.utils import get_int_from_datetime
import os

SECRET_JWT = os.environ.get('SECRET_JWT')

_secret_b64 = base64.urlsafe_b64encode(SECRET_JWT.encode('utf-8')).decode('utf-8') 

sign_key = jwk_from_dict({'kty': 'oct', 'k': _secret_b64})
jwt = JWT()

def generate_confirm_token(user_id):
    message = {
        'user_id': user_id,
        'exp': get_int_from_datetime(datetime.now(timezone.utc) + timedelta(hours=24)),
        'iat': get_int_from_datetime(datetime.now(timezone.utc))
    }
    return jwt.encode(message, sign_key, alg='HS256')