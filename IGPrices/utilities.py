from base64 import b64encode, b64decode
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import pandas as pd
import six

DATE_FORMATS = {1: "%Y:%m:%d-%H:%M:%S", 2: "%Y/%m/%d %H:%M:%S", 3: "%Y/%m/%d %H:%M:%S"}


def update_headers(existing_headers: dict, new_headers: dict) -> dict:
    for header in existing_headers.keys():
        if header in new_headers:
            existing_headers.update({header: new_headers[header]})
    return existing_headers


def encrypt_password(raw_password, key, timestamp):
    if key is not None:
        rsa_key = RSA.importKey(b64decode(key))
        string = raw_password + "|" + str(int(timestamp))
        message = b64encode(string.encode())
        return b64encode(PKCS1_v1_5.new(rsa_key).encrypt(message)).decode("utf-8"), True
    else:
        return raw_password, False


def conv_datetime(dt, version=1):
    try:
        if isinstance(dt, six.string_types):
            dt = pd.to_datetime(dt)
        fmt = DATE_FORMATS[int(version)]
        return dt.strftime(fmt)
    except (ValueError, TypeError):
        return dt
