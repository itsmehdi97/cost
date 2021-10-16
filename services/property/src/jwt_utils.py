import json
from datetime import datetime

from jose import jws
from jose.utils import base64url_decode


def is_expired(ts):
    return datetime.now().timestamp() > ts

def verify_token(token, secret):
    encoded_header, _, _ = token.split('.')
    header = json.loads(base64url_decode(encoded_header).decode())
    bytes_payload = jws.verify(token, secret, algorithms=[header['alg']])
    payload = json.loads(bytes_payload.decode())
    if is_expired(payload.get('exp')):
        return None
    return payload
