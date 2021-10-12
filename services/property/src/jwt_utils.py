from jose import jws
from jose.utils import base64url_decode
import json


def verify_token(token, secret):
    encoded_header, _, _ = token.split('.')
    header = json.loads(base64url_decode(encoded_header).decode())
    bytes_payload = jws.verify(token, secret, algorithms=[header['alg']])
    return json.loads(bytes_payload.decode())
