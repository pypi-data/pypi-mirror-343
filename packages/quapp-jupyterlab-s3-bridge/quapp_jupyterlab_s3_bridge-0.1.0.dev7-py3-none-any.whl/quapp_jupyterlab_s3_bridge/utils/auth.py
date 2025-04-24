# utils/auth.py
import re

def get_jwt_from_cookie(cookie_header, cookie_pattern="CognitoIdentityServiceProvider.*idToken"):
    if not cookie_header:
        return None
    pattern = re.compile(cookie_pattern)
    cookies = cookie_header.split(';')
    for cookie in cookies:
        if '=' not in cookie:
            continue
        name, value = cookie.strip().split('=', 1)
        if pattern.match(name.strip()):
            return value.strip()
    return None
