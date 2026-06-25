from pwdlib import PasswordHash
from fastapi.responses import JSONResponse
import re

password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def check_password_strenth(password):
    password_regex = r'^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]).{10,}$'
    if not re.match(password_regex, password):
        return JSONResponse(status_code=400,content={'error' : 'Password must be at least 10 characters with uppercase, lowercase, number, and special character'})